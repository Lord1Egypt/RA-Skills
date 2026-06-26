import json
import os
import sys
from typing import Dict, Any, List
from litellm import completion
from duckduckgo_search import DDGS

# Fix Windows console encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def search_ancestor(person_data: Dict[str, Any], model: str = "gemini/gemini-2.5-flash") -> Dict[str, Any]:
    """
    Autonomously researches an ancestor using web search and LLM extraction.
    Based on the autoresearch-genealogy methodology.
    """
    name = person_data.get("name", "")
    birth = person_data.get("birth_date", "")
    place = person_data.get("birth_place", "")
    
    if not name:
        return {"error": "Name is required for research."}
        
    # Extract just the main location (e.g., "Простоквашино" from "Простоквашино, Московская область")
    short_place = place.split(',')[0].strip() if place else ""
    
    print(f"Researching: {name} (b. {birth}, {short_place})")
    
    # 1. Formulate broader search queries
    queries = [
        f'{name} {birth} {short_place}',
        f'{name} {birth} genealogy',
    ]
    
    # Region-specific databases based on character sets or common names
    if any(char in name for char in "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"):
        # Russian / Soviet databases (broader queries without site: operator which DDG sometimes struggles with)
        queries.extend([
            f'{name} {birth} Память Народа',
            f'{name} {birth} ОБД Мемориал',
            f'{name} {birth} {short_place} Мемориал',
            f'{name} {birth} Бессмертный полк'
        ])
    else:
        # General English / US / UK databases
        queries.extend([
            f'{name} {birth} site:findagrave.com',
            f'{name} {birth} site:familysearch.org',
            f'{name} {birth} site:ancestry.com'
        ])
        
    all_results = []
    with DDGS() as ddgs:
        # Limit to top 4 queries to avoid rate limits
        search_queries = queries[-4:] if len(queries) > 4 else queries
        for query in search_queries:
            print(f"Searching: {query}")
            try:
                results = list(ddgs.text(query, max_results=3))
                all_results.extend(results)
            except Exception as e:
                print(f"Search failed for {query}: {e}")
                
    if not all_results:
        return {"status": "No new information found.", "person": person_data}
        
    # 2. Compile search results into a context string
    context = "\n\n".join([f"Title: {r.get('title')}\nSnippet: {r.get('body')}\nURL: {r.get('href')}" for r in all_results])
    
    # 3. Use LLM to extract new facts and verify against existing data
    prompt = f"""
    You are an expert genealogist following strict evidence-based methodology.
    
    Current known data for this person:
    {json.dumps(person_data, indent=2, ensure_ascii=False)}
    
    Web search results found:
    {context}
    
    Task:
    1. Analyze the search results to find NEW information about this person (death date, spouse, children, military service, etc.).
    2. Verify that the new information likely belongs to the SAME person (check dates and locations).
    3. Return an updated JSON object for this person, merging the old data with the new facts.
    4. Add a 'research_notes' field explaining what was found and citing the URLs.
    5. If no new reliable information is found, return the original data unchanged.
    
    Return ONLY valid JSON matching the original structure, plus 'research_notes'.
    """
    
    try:
        response = completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        updated_data = json.loads(response.choices[0].message.content)
        return {"status": "Research complete", "person": updated_data}
    except Exception as e:
        return {"error": f"LLM extraction failed: {e}", "person": person_data}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        person_id = sys.argv[2] if len(sys.argv) > 2 else None
        
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if person_id:
            # Research specific person
            person = next((p for p in data.get("people", []) if p["id"] == person_id), None)
            if person:
                result = search_ancestor(person)
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Person {person_id} not found.")
        else:
            # Research first person as demo
            if data.get("people"):
                result = search_ancestor(data["people"][0])
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print("No people found in data.")
    else:
        print("Usage: python research.py input_data.json [person_id]")
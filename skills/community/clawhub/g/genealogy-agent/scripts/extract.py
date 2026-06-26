import json
import os
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from litellm import completion

class Person(BaseModel):
    id: str = Field(description="Unique identifier (e.g., 'ivan_ivanov')")
    name: str = Field(description="Full name")
    birth_date: Optional[str] = Field(description="Birth date or year")
    death_date: Optional[str] = Field(description="Death date or year")
    birth_place: Optional[str] = Field(description="Birth place")
    notes: Optional[str] = Field(description="Additional biographical notes")

class Relationship(BaseModel):
    source_id: str = Field(description="ID of the person (e.g., 'ivan_ivanov')")
    target_id: str = Field(description="ID of the related person (e.g., 'maria_ivanova')")
    type: str = Field(description="Relationship type (e.g., 'parent', 'child', 'spouse', 'sibling')")

class FamilyData(BaseModel):
    people: List[Person]
    relationships: List[Relationship]

def extract_family_data(text: str, model: str = "gemini/gemini-2.5-flash") -> Dict[str, Any]:
    """Extracts structured family data from raw text using an LLM."""
    prompt = f"""
    Extract all people, their biographical details (birth/death dates, places), and their relationships from the following text.
    Return the data as a structured JSON object with 'people' and 'relationships' lists.
    Use consistent IDs for people (e.g., lowercase names with underscores).
    
    Text:
    {text}
    """
    
    response = completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format=FamilyData,
    )
    
    # litellm returns a Pydantic object if response_format is used
    data = response.choices[0].message.content
    if isinstance(data, str):
        return json.loads(data)
    return data.model_dump()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        text = sys.argv[1]
        print(json.dumps(extract_family_data(text), indent=2, ensure_ascii=False))
    else:
        print("Usage: python extract.py 'raw text about family history'")
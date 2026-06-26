import requests
import os
from dotenv import load_dotenv
from typing import Dict, List, Optional

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print(f"Warning: .env file not found at {dotenv_path}")

# Import PDF analyzer and Zotero archiver
from .pdf_analyzer import analyze_pdf_header, analyze_pdf_fulltext

# Create a directory for downloaded PDFs
PDF_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pdfs')
if not os.path.exists(PDF_DIR):
    os.makedirs(PDF_DIR)


def download_pdf(url: str, filename: str) -> Optional[str]:
    """Download PDF from URL and save to file
    
    Args:
        url: URL of the PDF file
        filename: Filename to save the PDF
    
    Returns:
        Path to the downloaded PDF file, or None if download failed
    """
    try:
        # Full path to save the PDF
        pdf_path = os.path.join(PDF_DIR, filename)
        
        # Send GET request to download PDF
        response = requests.get(url, timeout=60)
        
        # Check if request was successful
        if response.status_code == 200:
            # Save PDF to file
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded PDF: {pdf_path}")
            return pdf_path
        else:
            print(f"Failed to download PDF: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading PDF: {e}")
        return None


def search_semantic_scholar(query, limit=10):
    """Search papers from Semantic Scholar"""
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": query,
        "limit": limit,
        "fields": "title,abstract,authors,year,venue,url,externalIds,publicationTypes,referenceCount,citationCount,influentialCitationCount"
    }

    # Get API key from environment variable
    api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    headers = {}
    if api_key:
        headers["x-api-key"] = api_key

    try:
        res = requests.get(url, params=params, headers=headers, timeout=30)
        res.raise_for_status()
        data = res.json()

        papers = []
        for p in data.get("data", []):
            # Extract PDF URL if available
            pdf_url = None
            external_ids = p.get("externalIds", {})
            if external_ids.get("ArXiv"):
                arxiv_id = external_ids["ArXiv"]
                pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            elif p.get("url"):
                # Try to construct PDF URL from the paper URL
                if "semanticscholar.org" in p.get("url"):
                    pdf_url = p.get("url") + ".pdf"
            
            paper = {
                "title": p.get("title"),
                "abstract": p.get("abstract"),
                "authors": [a["name"] for a in p.get("authors", [])],
                "year": p.get("year"),
                "doi": p.get("doi"),
                "url": p.get("url"),
                "pdf_url": pdf_url,
                "publication_types": p.get("publicationTypes"),
                "reference_count": p.get("referenceCount"),
                "citation_count": p.get("citationCount"),
                "influential_citation_count": p.get("influentialCitationCount"),
                "external_ids": external_ids,
                "source": "semantic_scholar",
                "raw_data": p  # Store original data
            }
            papers.append(paper)

        if not papers:
            print("Semantic Scholar returned no results")
            if not api_key:
                print("Note: Semantic Scholar API may have rate limits without an API key")
        
        return papers
    except requests.exceptions.RequestException as e:
        print(f"Error searching Semantic Scholar: {e}")
        if not api_key:
            print("Note: Semantic Scholar API may have rate limits without an API key")
        return []


def search_arxiv(query, limit=10):
    """Search papers from arXiv (computer science category)"""
    url = "http://export.arxiv.org/api/query"

    # arXiv API doesn't support wildcards (cs.*), use a different approach
    # arXiv API defaults to OR for space-separated terms
    # We need to explicitly AND all terms for correct semantics
    query_terms = query.split()
    if len(query_terms) > 1:
        # Build AND query: all:term1 AND all:term2 AND ...
        search_query = " AND ".join([f"all:{term}" for term in query_terms])
    else:
        # Single term, just use all:query
        search_query = f"all:{query}"

    params = {
        "search_query": search_query,
        "max_results": limit * 2,  # Get extra results for filtering
        "sortBy": "submittedDate",  # Sort by submission date
        "sortOrder": "descending"    # Newest first
    }
    
    try:
        res = requests.get(url, params=params, timeout=30)
        res.raise_for_status()
        
        # Parse XML response
        import xml.etree.ElementTree as ET
        root = ET.fromstring(res.content)

        papers = []
        query_terms = query.lower().split()
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text
            abstract = entry.find('{http://www.w3.org/2005/Atom}summary').text

            # Filter: only keep papers that have ALL query terms in title or abstract (AND semantics)
            # This removes irrelevant papers that got through due to API limitations
            text = (title + " " + abstract).lower()
            # Only check terms longer than 3 characters (skip stop words like "a", "the", "of")
            filtered_terms = [term for term in query_terms if len(term) > 3]
            # If no terms to check, accept all
            if not filtered_terms:
                has_match = True
            else:
                # Require ALL terms to be present (AND semantics)
                has_match = all(term in text for term in filtered_terms)
            if not has_match:
                continue

            # Extract authors
            authors = []
            for author in entry.findall('{http://www.w3.org/2005/Atom}author'):
                authors.append(author.find('{http://www.w3.org/2005/Atom}name').text)
            
            # Extract year from published date
            published = entry.find('{http://www.w3.org/2005/Atom}published').text
            year = published.split('-')[0] if published else None
            
            # Extract URL and PDF URL
            url = None
            pdf_url = None
            for link in entry.findall('{http://www.w3.org/2005/Atom}link'):
                if link.get('rel') == 'alternate':
                    url = link.get('href')
                elif link.get('type') == 'application/pdf':
                    pdf_url = link.get('href')
            
            # Extract category
            categories = []
            for category in entry.findall('{http://www.w3.org/2005/Atom}category'):
                categories.append(category.get('term'))
            
            # Extract arXiv ID
            arxiv_id = None
            id_element = entry.find('{http://www.w3.org/2005/Atom}id')
            if id_element is not None:
                id_text = id_element.text
                if id_text:
                    arxiv_id = id_text.split('/')[-1]
            
            # Extract updated date
            updated = entry.find('{http://www.w3.org/2005/Atom}updated').text if entry.find('{http://www.w3.org/2005/Atom}updated') is not None else None
            
            # Store original entry data
            raw_data = {}
            for child in entry:
                tag = child.tag.replace('{http://www.w3.org/2005/Atom}', '')
                if tag == 'author':
                    if 'authors' not in raw_data:
                        raw_data['authors'] = []
                    raw_data['authors'].append(child.find('{http://www.w3.org/2005/Atom}name').text)
                elif tag == 'link':
                    if 'links' not in raw_data:
                        raw_data['links'] = []
                    raw_data['links'].append({
                        'href': child.get('href'),
                        'rel': child.get('rel'),
                        'type': child.get('type')
                    })
                elif tag == 'category':
                    if 'categories' not in raw_data:
                        raw_data['categories'] = []
                    raw_data['categories'].append(child.get('term'))
                else:
                    raw_data[tag] = child.text
            
            papers.append({
                "title": title,
                "abstract": abstract,
                "authors": authors,
                "year": year,
                "url": url,
                "pdf_url": pdf_url,
                "categories": categories,
                "arxiv_id": arxiv_id,
                "updated": updated,
                "source": "arxiv",
                "raw_data": raw_data  # Store original data
            })
        # Trim to requested limit after filtering
        papers = papers[:limit]

        if not papers:
            print("arXiv returned no results")

        return papers
    except requests.exceptions.RequestException as e:
        print(f"Error searching arXiv: {e}")
        return []
    except ET.ParseError as e:
        print(f"Error parsing arXiv XML response: {e}")
        return []


def search_google_scholar(query, limit=10):
    """Search papers from Google Scholar (using SerpAPI)"""
    # Note: Google Scholar doesn't have an official API
    # This implementation uses SerpAPI, which requires an API key
    # You can get a free API key at https://serpapi.com/
    
    # Get API key from environment variable
    serpapi_key = os.getenv("SERPAPI_KEY")
    
    if not serpapi_key:
        print("Warning: Google Scholar search requires a SerpAPI key")
        print("Set the SERPAPI_KEY environment variable with your API key")
        print("Get a free API key at https://serpapi.com/")
        return []
    
    url = "https://serpapi.com/search.json"
    
    # Match the parameters from the web URL
    params = {
        "engine": "google_scholar",
        "q": query,
        "num": limit,
        "hl": "zh-CN",  # Chinese language
        "as_sdt": "0,5",  # Search type parameters
        "api_key": serpapi_key
    }
    
    try:
        res = requests.get(url, params=params, timeout=30)
        res.raise_for_status()
        data = res.json()
        
        # Check if there's an error in the response
        if "error" in data:
            print(f"Google Scholar API error: {data['error']}")
            return []
        
        papers = []
        for result in data.get("organic_results", []):
            # Extract authors
            authors = []
            if "authors" in result:
                if isinstance(result["authors"], list):
                    # Check if authors are dictionaries with 'name' field
                    for author in result["authors"]:
                        if isinstance(author, dict) and "name" in author:
                            authors.append(author["name"])
                        elif isinstance(author, str):
                            authors.append(author)
                else:
                    authors = [author.strip() for author in result["authors"].split(",") if author.strip()]
            elif "publication_info" in result and "authors" in result["publication_info"]:
                if isinstance(result["publication_info"]["authors"], list):
                    # Check if authors are dictionaries with 'name' field
                    for author in result["publication_info"]["authors"]:
                        if isinstance(author, dict) and "name" in author:
                            authors.append(author["name"])
                        elif isinstance(author, str):
                            authors.append(author)
                else:
                    authors = [author.strip() for author in result["publication_info"]["authors"].split(",") if author.strip()]
            
            # Extract year
            year = None
            if "publication_info" in result:
                if "year" in result["publication_info"]:
                    year = result["publication_info"].get("year")
                elif "summary" in result["publication_info"]:
                    # Try to extract year from summary
                    import re
                    year_match = re.search(r'(19|20)\d{2}', result["publication_info"]["summary"])
                    if year_match:
                        year = year_match.group(0)
            elif "year" in result:
                year = result.get("year")
            
            # Extract PDF URL if available
            pdf_url = None
            if "resources" in result:
                for resource in result["resources"]:
                    if resource.get("file_format") == "PDF":
                        pdf_url = resource.get("link")
                        break
            
            # Extract additional information
            publication_info = result.get("publication_info", {})
            venue = publication_info.get("summary")
            citations = result.get("inline_links", {}).get("cited_by", {}).get("total")
            related_pages = result.get("inline_links", {}).get("related_pages", {}).get("total")
            
            papers.append({
                "title": result.get("title"),
                "abstract": result.get("snippet"),
                "authors": authors,
                "year": year,
                "url": result.get("link"),
                "pdf_url": pdf_url,
                "venue": venue,
                "citations": citations,
                "related_pages": related_pages,
                "publication_info": publication_info,
                "source": "google_scholar",
                "raw_data": result  # Store original data
            })
        
        if not papers:
            print("Google Scholar returned no results")
        
        return papers
    except requests.exceptions.RequestException as e:
        print(f"Error searching Google Scholar: {e}")
        return []
    except ValueError as e:
        print(f"Error parsing Google Scholar API response: {e}")
        return []


def search_tavily(query, limit=10):
    """Search papers from Tavily (focused on academic literature)"""
    # Get API key from environment variable
    api_key = os.getenv("TAVILY_API_KEY")
    
    if not api_key:
        print("Warning: Tavily search requires an API key")
        print("Set the TAVILY_API_KEY environment variable with your API key")
        print("Get a free API key at https://tavily.com/")
        return []
    
    url = "https://api.tavily.com/search"
    
    # According to Tavily API documentation, optimized for academic literature
    headers = {
        "Content-Type": "application/json"
    }
    
    # Optimize search parameters for academic literature
    payload = {
        "api_key": api_key,
        "query": f"academic paper {query}",  # Add context to focus on academic papers
        "limit": limit,
        "search_depth": "advanced",
        "include_answer": False,
        "include_images": False,
        "include_raw_content": False,
        "topic": "general"  # Use valid topic value
    }
    
    try:
        # Use POST request as recommended by Tavily API docs
        res = requests.post(url, json=payload, headers=headers, timeout=30)
        res.raise_for_status()
        
        try:
            data = res.json()
        except ValueError:
            print("Error parsing Tavily API response")
            return []
        
        # Check if there's an error in the response
        if "error" in data:
            print(f"Tavily API error: {data['error']}")
            return []
        
        papers = []
        for result in data.get("results", []):
            # Extract authors if available (very conservative approach)
            authors = []
            import re
            content = result.get("content", "")
            
            # Only extract authors if we find a clear author pattern
            # Look for patterns like "Authors: John Doe, Jane Smith"
            author_pattern = r'\bAuthors?:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:,\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)*)'
            match = re.search(author_pattern, content, re.IGNORECASE)
            if match:
                author_text = match.group(1).strip()
                # Split by commas
                author_list = [author.strip() for author in author_text.split(',')]
                # Only keep valid author names (at least 2 words)
                authors = [author for author in author_list if len(author.split()) >= 2]
            
            # Extract year if available
            year = None
            # Try to extract year from content or title
            content_with_title = content + " " + result.get("title", "")
            year_match = re.search(r'(19|20)\d{2}', content_with_title)
            if year_match:
                year = year_match.group(0)
            
            # Extract additional information
            source_type = "academic" if any(term in content.lower() for term in ["doi", "journal", "paper", "research", "arxiv", "pmc", "sciencedirect"]) else "web"
            relevance_score = result.get("score", 0)
            
            # Determine if it's a PDF
            is_pdf = result.get("url", "").endswith(".pdf")
            
            # Extract PDF URL if available
            pdf_url = result.get("url") if is_pdf else None
            
            # Add domain information
            domain = result.get("url", "").split('//')[-1].split('/')[0] if result.get("url") else ""
            
            # Extract additional metadata
            published_date = None
            # Try to extract published date from content
            date_pattern = r'(?:Published|Published on|Date):\s*([\d]{4}-[\d]{2}-[\d]{2}|[\d]{2}/[\d]{2}/[\d]{4})'
            date_match = re.search(date_pattern, content, re.IGNORECASE)
            if date_match:
                published_date = date_match.group(1)
            
            # Extract DOI if available
            doi = None
            doi_pattern = r'\bDOI:\s*(10\.\d{4,}/[-._;()/\w]+)'
            doi_match = re.search(doi_pattern, content)
            if doi_match:
                doi = doi_match.group(1)
            
            papers.append({
                "title": result.get("title"),
                "abstract": result.get("content"),  # Use content instead of snippet
                "authors": authors,
                "year": year,
                "url": result.get("url"),
                "pdf_url": pdf_url,
                "source_type": source_type,
                "relevance_score": relevance_score,
                "is_pdf": is_pdf,
                "domain": domain,
                "published_date": published_date,
                "doi": doi,
                "source": "tavily",
                "raw_data": result  # Store original data
            })
        
        if not papers:
            print("Tavily returned no results")
        
        return papers
    except requests.exceptions.RequestException as e:
        print(f"Error searching Tavily: {e}")
        return []


def search_papers(query, limit=10, source="all", download_pdf_flag=False, per_source_limit=None, engine_weights=None):
    """Search papers from multiple sources with engine weight distribution
    
    Args:
        query: Search query
        limit: Maximum number of total results
        source: Source to search from ("all", "semantic_scholar", "arxiv", "google_scholar", "tavily")
        download_pdf_flag: Whether to download PDF files (if available)
        per_source_limit: Maximum number of results per source (only applies when source="all")
        engine_weights: Dictionary of engine weights (only applies when source="all")
    
    Returns:
        List of papers with additional information
    """
    papers = []
    
    # Default engine weights: arXiv (5), Google Scholar (3), Semantic Scholar (1), Tavily (1)
    if engine_weights is None:
        engine_weights = {
            "arxiv": 5,
            "google_scholar": 3,
            "semantic_scholar": 1,
            "tavily": 1
        }
    
    print(f"Using engine weights: {engine_weights}")
    
    # Calculate per-engine limits based on weights
    if source == "all" and engine_weights:
        # Calculate total weight
        total_weight = sum(engine_weights.values())
        print(f"Total weight: {total_weight}")
        # Calculate number of results per engine
        source_limits = {}
        remaining_limit = limit
        
        # First distribute based on weights
        for src, weight in engine_weights.items():
            if source == "all" or source == src:
                count = max(1, int(limit * weight / total_weight))
                source_limits[src] = count
                remaining_limit -= count
                print(f"Assigned {count} results to {src}")
        
        # Distribute remaining results
        if remaining_limit > 0:
            print(f"Distributing {remaining_limit} remaining results")
            # Sort engines by weight in descending order
            sorted_sources = sorted(engine_weights.items(), key=lambda x: x[1], reverse=True)
            for i in range(remaining_limit):
                src = sorted_sources[i % len(sorted_sources)][0]
                if source == "all" or source == src:
                    source_limits[src] = source_limits.get(src, 0) + 1
                    print(f"Added 1 more result to {src}")
    else:
        # Use per_source_limit or limit for single source
        source_limit = per_source_limit if per_source_limit else limit
        source_limits = {source: source_limit} if source != "all" else {}
    
    print(f"Final source limits: {source_limits}")
    
    # Search each source with its limit
    if (source == "all" or source == "semantic_scholar") and "semantic_scholar" in source_limits:
        print(f"Searching Semantic Scholar with limit {source_limits['semantic_scholar']}")
        semantic_papers = search_semantic_scholar(query, source_limits["semantic_scholar"])
        print(f"Semantic Scholar returned {len(semantic_papers)} papers")
        papers.extend(semantic_papers)
    
    if (source == "all" or source == "arxiv") and "arxiv" in source_limits:
        print(f"Searching arXiv with limit {source_limits['arxiv']}")
        arxiv_papers = search_arxiv(query, source_limits["arxiv"])
        print(f"arXiv returned {len(arxiv_papers)} papers")
        papers.extend(arxiv_papers)
    
    if (source == "all" or source == "google_scholar") and "google_scholar" in source_limits:
        print(f"Searching Google Scholar with limit {source_limits['google_scholar']}")
        google_papers = search_google_scholar(query, source_limits["google_scholar"])
        print(f"Google Scholar returned {len(google_papers)} papers")
        papers.extend(google_papers)
    
    if (source == "all" or source == "tavily") and "tavily" in source_limits:
        print(f"Searching Tavily with limit {source_limits['tavily']}")
        tavily_papers = search_tavily(query, source_limits["tavily"])
        print(f"Tavily returned {len(tavily_papers)} papers")
        papers.extend(tavily_papers)
    
    print(f"Total papers found: {len(papers)}")
    
    # Process each paper
    processed_papers = []
    seen_titles = set()  # To avoid duplicates
    
    for paper in papers:
        # Skip duplicates based on title
        title = paper.get("title", "")
        if title and title in seen_titles:
            continue
        seen_titles.add(title)
        
        # Add source information if not already present
        if "source" not in paper:
            paper["source"] = source if source != "all" else "mixed"
        
        # Ensure URL is correct for the source
        if "url" in paper:
            # No need to modify URL as each search function already returns the correct URL for its source
            pass
        
        # Validate PDF URL
        if "pdf_url" in paper and paper["pdf_url"]:
            # Basic validation: check if it's a valid URL
            if not paper["pdf_url"].startswith(('http://', 'https://')):
                print(f"Warning: Invalid PDF URL format: {paper['pdf_url']}")
        
        # Download PDF if requested and PDF URL is available
        if download_pdf_flag and "pdf_url" in paper and paper["pdf_url"]:
            # Generate filename for PDF
            title = paper.get("title", "unknown").replace(' ', '_').replace('/', '_').replace('\\', '_')
            filename = f"{title}_{paper.get('year', 'unknown')}.pdf"
            # Download PDF
            pdf_path = download_pdf(paper["pdf_url"], filename)
            if pdf_path:
                paper["pdf_path"] = pdf_path
        
        processed_papers.append(paper)
        
        # Stop if we've reached the limit
        if len(processed_papers) >= limit:
            break
    
    # Print source distribution
    source_counts = {}
    for paper in processed_papers:
        src = paper.get("source", "unknown")
        source_counts[src] = source_counts.get(src, 0) + 1
    print(f"Source distribution: {source_counts}")
    
    # Print details of each paper including source
    print("\nDetailed results:")
    for i, paper in enumerate(processed_papers, 1):
        print(f"\nPaper {i}:")
        print(f"Title: {paper.get('title', 'N/A')}")
        print(f"Source: {paper.get('source', 'N/A')}")
        print(f"URL: {paper.get('url', 'N/A')}")
        print(f"PDF URL: {paper.get('pdf_url', 'N/A')}")
    
    return processed_papers


if __name__ == '__main__':
    # Test Semantic Scholar search
    print("=== Semantic Scholar Results ===")
    papers = search_papers('hallucination', limit=2, source="semantic_scholar")
    for p in papers:
        print(p)
    
    # Test arXiv search
    print("\n=== arXiv Results ===")
    papers = search_papers('hallucination', limit=2, source="arxiv")
    for p in papers:
        print(p)
    
    # Test Google Scholar search
    print("\n=== Google Scholar Results ===")
    papers = search_papers('hallucination', limit=2, source="google_scholar")
    for p in papers:
        print(p)
    
    # Test Tavily search
    print("\n=== Tavily Results ===")
    papers = search_papers('hallucination', limit=2, source="tavily")
    for p in papers:
        print(p)
    
    # Test all sources
    print("\n=== All Sources Results ===")
    papers = search_papers('hallucination', limit=5, source="all")
    for p in papers:
        print(p)

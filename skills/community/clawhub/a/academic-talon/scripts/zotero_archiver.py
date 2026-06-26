import requests
import os
from dotenv import load_dotenv
from typing import Dict, Optional

# Try to import pyzotero
try:
    from pyzotero import Zotero
except ImportError:
    print("pyzotero not installed. Using direct API calls instead.")
    Zotero = None

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print(f"Warning: .env file not found at {dotenv_path}")


def detect_item_type(paper_info: Dict) -> str:
    """Detect item type based on paper information

    Args:
        paper_info: Dictionary containing paper information

    Returns:
        Zotero item type string
    """
    # Check what type of publication this is
    journal = paper_info.get('journal')
    conference = paper_info.get('conference')
    arxiv_id = paper_info.get('arxiv_id')

    # If it's an arXiv preprint with no journal/conference, use preprint type
    if arxiv_id and not journal and not conference:
        return "preprint"
    # If it's a conference paper, use conferencePaper
    elif conference:
        return "conferencePaper"
    # If it's a journal article, use journalArticle
    elif journal:
        return "journalArticle"
    # Default to preprint for unknown types
    elif arxiv_id:
        return "preprint"
    # Default to journalArticle
    else:
        return "journalArticle"


def find_duplicate(paper_info: Dict, api_key: str, library_id: str, library_type: str = "user") -> list:
    """Find existing papers that match this paper in Zotero library

    Args:
        paper_info: Dictionary containing paper information
        api_key: Zotero API key
        library_id: Zotero library ID
        library_type: Zotero library type ("user" or "group")

    Returns:
        List of existing matching items, empty list if no duplicates found
    """
    duplicates = []
    # Check by DOI first if available
    doi = paper_info.get("doi")
    if doi:
        url = f"https://api.zotero.org/{library_type}s/{library_id}/items"
        params = {"q": doi}
        headers = {
            "Zotero-API-Key": api_key
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            items = response.json()
            if len(items) > 0:
                print(f"Duplicate found by DOI: {doi}")
                return items
        except Exception as e:
            print(f"Error checking for duplicate by DOI: {e}")

    # Check by title and authors if DOI is not available or check failed
    title = paper_info.get("title")
    authors = paper_info.get("authors", [])

    if title:
        # Search by title
        url = f"https://api.zotero.org/{library_type}s/{library_id}/items"
        params = {"q": title}
        headers = {
            "Zotero-API-Key": api_key
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            items = response.json()
            print(f"Searching for duplicate by title: {title}")
            print(f"Found {len(items)} items")

            # Check if any item with the same title has matching authors
            for item in items:
                item_data = item.get("data", {})
                item_title = item_data.get("title")
                print(f"Found item: {item_title}")
                if item_title and item_title.lower() == title.lower():
                    # Check if authors match
                    item_creators = item_data.get("creators", [])
                    item_authors = [f"{c.get('firstName', '')} {c.get('lastName', '')}".strip() for c in item_creators if c.get('creatorType') == 'author']
                    print(f"Item authors: {item_authors}")
                    print(f"Paper authors: {authors}")

                    # If at least one author matches, consider it a duplicate
                    if any(author in item_authors for author in authors):
                        print("Duplicate found by title and authors")
                        duplicates.append(item)
                        break

        except Exception as e:
            print(f"Error checking for duplicate by title: {e}")

    return duplicates


def create_item(paper_info: Dict, api_key: str, library_id: str, library_type: str = "user") -> Dict:
    """Create item in Zotero library
    
    Args:
        paper_info: Dictionary containing paper information
        api_key: Zotero API key
        library_id: Zotero library ID
        library_type: Zotero library type ("user" or "group")
        
    Returns:
        Response from Zotero API
    """
    url = f"https://api.zotero.org/{library_type}s/{library_id}/items"
    
    headers = {
        "Zotero-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    item_type = detect_item_type(paper_info)
    
    item = {
        "itemType": item_type,
        "title": paper_info.get("title", ""),
        "abstractNote": paper_info.get("abstract", ""),
        "url": paper_info.get("url", ""),
        "DOI": paper_info.get("doi", ""),
        "date": paper_info.get("year", ""),
        "creators": []
    }
    
    # Add authors
    authors = paper_info.get("authors", [])
    for author in authors:
        # Split author name into first and last name
        name_parts = author.split()
        if len(name_parts) >= 2:
            last_name = name_parts[-1]
            first_name = " ".join(name_parts[:-1])
        else:
            last_name = author
            first_name = ""
        
        item["creators"].append({
            "creatorType": "author",
            "firstName": first_name,
            "lastName": last_name
        })
    
    # Add venue information
    venue = paper_info.get("venue", "")
    if venue:
        item["publicationTitle"] = venue
    
    # Add keywords
    keywords = paper_info.get("keywords", [])
    if keywords:
        item["tags"] = [{'tag': keyword} for keyword in keywords]
    
    # Add BibTeX info if available
    if "bibtex" in paper_info:
        item["extra"] = paper_info["bibtex"]
    
    try:
        response = requests.post(url, json=[item], headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error creating item: {e}")
        return {"error": str(e)}


def get_collection_id(zot: 'Zotero', collection_name: str) -> Optional[str]:
    """Get collection ID by name
    
    Args:
        zot: Zotero client instance
        collection_name: Name of the collection
        
    Returns:
        Collection ID if found, None otherwise
    """
    try:
        collections = zot.collections()
        # Check if collections is a list
        if not isinstance(collections, list):
            print(f"Unexpected collections format: {type(collections)}")
            return None
        
        for collection in collections:
            # Check if collection is a dictionary
            if not isinstance(collection, dict):
                print(f"Unexpected collection format: {type(collection)}")
                continue
            
            # Get key directly from collection
            if collection.get('name') == collection_name:
                return collection.get('key')
            # Fallback to checking data field
            elif collection.get('data', {}).get('name') == collection_name:
                return collection.get('key')
        return None
    except Exception as e:
        print(f"Error getting collection ID: {e}")
        return None

def create_collection(zot: 'Zotero', collection_name: str) -> Optional[str]:
    """Create a new collection

    Args:
        zot: Zotero client instance
        collection_name: Name of the collection

    Returns:
        Collection ID if created successfully, None otherwise
    """
    try:
        collection = zot.create_collections([{'name': collection_name}])
        # Handle different response formats from pyzotero
        if isinstance(collection, list) and len(collection) > 0:
            # List format: each created collection is a dict with 'key'
            first_collection = collection[0]
            if isinstance(first_collection, dict) and 'key' in first_collection:
                return first_collection['key']
        elif isinstance(collection, dict) and 'successful' in collection:
            # Dict format: successful is dict {key: data}
            successful_collections = collection['successful']
            if successful_collections and isinstance(successful_collections, dict):
                first_key = next(iter(successful_collections))
                return first_key
        elif isinstance(collection, dict) and 'key' in collection:
            # Direct dict format
            return collection['key']
        return None
    except Exception as e:
        print(f"Error creating collection: {e}")
        return None

def add_to_collection(zot: 'Zotero', item_key: str, collection_id: str) -> bool:
    """Add item to collection
    
    Args:
        zot: Zotero client instance
        item_key: Item key
        collection_id: Collection ID
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Print debug information
        print(f"Adding item {item_key} to collection {collection_id}")
        
        # Try a different approach using the collections API directly
        # Instead of using zot.addto_collection, use the items API to update the item's collections
        item = zot.item(item_key)
        if isinstance(item, dict):
            # Get existing collections
            collections = item.get('data', {}).get('collections', [])
            if not isinstance(collections, list):
                collections = []
            
            # Add the collection ID if it's not already there
            if collection_id not in collections:
                collections.append(collection_id)
                # Update the item with the new collections
                item['data']['collections'] = collections
                update_result = zot.update_item(item)
                print(f"Update result: {update_result}")
                return True
            else:
                print("Item already in collection")
                return True
        else:
            print(f"Unexpected item format: {type(item)}")
            return False
    except Exception as e:
        print(f"Error adding item to collection: {e}")
        import traceback
        traceback.print_exc()
        return False

def archive_paper(paper_info: Dict, zotero_api_key: Optional[str] = None, zotero_library_id: Optional[str] = None, zotero_library_type: str = "user", use_pyzotero: bool = False, collection: str = "openclaw") -> Dict:
    """Archive paper to Zotero
    
    Args:
        paper_info: Dictionary containing paper information
        zotero_api_key: Zotero API key (optional, will use environment variable if not provided)
        zotero_library_id: Zotero library ID (optional, will use environment variable if not provided)
        zotero_library_type: Zotero library type ("user" or "group")
        use_pyzotero: Whether to use pyzotero library for archiving
        collection: Name of the collection to add the paper to (default: "openclaw")
        
    Returns:
        Dictionary with archiving result
    """
    # Get API key and library ID from environment variables if not provided
    if not zotero_api_key:
        zotero_api_key = os.getenv("ZOTERO_API_KEY")
    
    if not zotero_library_id:
        zotero_library_id = os.getenv("ZOTERO_LIBRARY_ID")
    
    if not zotero_api_key or not zotero_library_id:
        error_msg = "Zotero API key or library ID not provided"
        return {"error": error_msg}
    
    # Use pyzotero if requested and available
    if use_pyzotero and Zotero:
        try:
            # Initialize pyzotero client
            zot = Zotero(zotero_library_id, zotero_library_type, zotero_api_key)
            
            # Check for duplicate
            # First check by DOI if available
            doi = paper_info.get("doi")
            if doi:
                try:
                    # Search by DOI
                    items = zot.items(q=doi)
                    if items:
                        print(f"Duplicate found by DOI: {doi}")
                        # Already exists, try to add to collection if not already there
                        if collection:
                            # Get the first existing item
                            if items:
                                if 'key' in items[0]:
                                    item_key = items[0]['key']
                                    coll_id = get_collection_id(zot, collection)
                                    if not coll_id:
                                        coll_id = create_collection(zot, collection)
                                    if coll_id:
                                        if add_to_collection(zot, item_key, coll_id):
                                            return {
                                                "success": True,
                                                "item_id": item_key,
                                                "added_to_collection": True,
                                                "message": "Paper already existed, added to collection"
                                            }
                        return {"error": "Paper already exists in Zotero library"}
                except Exception as e:
                    print(f"Error checking duplicate by DOI: {e}")

            # Check by title and authors if DOI is not available
            title = paper_info.get("title")
            authors = paper_info.get("authors", [])
            if title:
                try:
                    # Search by title
                    items = zot.items(q=title)
                    print(f"Searching for duplicate by title: {title}")
                    print(f"Found {len(items)} items")
                    for item in items:
                        item_data = item.get("data", {})
                        item_title = item_data.get("title")
                        print(f"Found item: {item_title}")
                        if item_title and item_title.lower() == title.lower():
                            # Check if authors match
                            item_creators = item_data.get("creators", [])
                            item_authors = [f"{c.get('firstName', '')} {c.get('lastName', '')}".strip() for c in item_creators if c.get('creatorType') == 'author']
                            print(f"Item authors: {item_authors}")
                            print(f"Paper authors: {authors}")
                            # If at least one author matches, consider it a duplicate
                            if any(author in item_authors for author in authors):
                                print("Duplicate found by title and authors")
                                # Already exists, try to add to collection if not already there
                                if collection:
                                    if 'key' in item:
                                        item_key = item['key']
                                        coll_id = get_collection_id(zot, collection)
                                        if not coll_id:
                                            coll_id = create_collection(zot, collection)
                                        if coll_id:
                                            if add_to_collection(zot, item_key, coll_id):
                                                return {
                                                    "success": True,
                                                    "item_id": item_key,
                                                    "added_to_collection": True,
                                                    "message": "Paper already existed, added to collection"
                                                }
                                return {"error": "Paper already exists in Zotero library"}
                except Exception as e:
                    print(f"Error checking duplicate by title and authors: {e}")
            
            # Prepare item data
            creators = []
            for author in paper_info.get("authors", []):
                # Check if already in "Lastname, Firstname" format from BibTeX
                if ',' in author:
                    parts = author.split(',', 1)
                    last_name = parts[0].strip()
                    first_name = parts[1].strip()
                else:
                    name_parts = author.split()
                    if len(name_parts) >= 2:
                        first_name = " ".join(name_parts[:-1])
                        last_name = name_parts[-1]
                    else:
                        first_name = ""
                        last_name = author
                creators.append({"creatorType": "author", "firstName": first_name, "lastName": last_name})

            journal = paper_info.get('journal')
            conference = paper_info.get('conference')
            arxiv_id = paper_info.get('arxiv_id')

            # Get PDF base URL from environment
            pdf_base_url = os.getenv("PDF_BASE_URL")
            # Check if we have a local PDF
            # Generate filename from citation key
            from scripts.pdf_analyzer import generate_bibtex_citation_key
            citation_key = generate_bibtex_citation_key(paper_info)
            local_pdf_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'pdfs',
                f"{citation_key}.pdf"
            )
            # If PDF exists locally and PDF_BASE_URL is configured, use local URL
            url = paper_info.get("url", "")
            if pdf_base_url and os.path.exists(local_pdf_path):
                # Construct local URL
                local_pdf_url = pdf_base_url.rstrip('/') + f"/{citation_key}.pdf"
                url = local_pdf_url
                print(f"Using local PDF URL: {local_pdf_url}")

            item_data = {
                "itemType": detect_item_type(paper_info),
                "title": paper_info.get("title", ""),
                "creators": creators,
                "abstractNote": paper_info.get("abstract", ""),
                "date": paper_info.get("year", ""),
                "url": url,
                "DOI": paper_info.get("doi", "")
            }

            # Add publication title (journal/conference name)
            if journal:
                item_data["publicationTitle"] = journal
            elif conference:
                item_data["publicationTitle"] = conference

            # Add arXiv info to extra if available
            extra_parts = []
            if arxiv_id:
                clean_arxiv_id = arxiv_id.replace('arXiv:', '').replace('arXiv', '').split('[')[0].strip()
                if clean_arxiv_id:
                    extra_parts.append(f"arXiv:{clean_arxiv_id}")
                    # Only override URL if no local PDF available
                    if not pdf_base_url or not os.path.exists(local_pdf_path):
                        item_data["url"] = f"https://arxiv.org/abs/{clean_arxiv_id}"

            # Add BibTeX info if available
            if "bibtex" in paper_info:
                extra_parts.append(paper_info["bibtex"])

            if extra_parts:
                item_data["extra"] = "\n".join(extra_parts)

            # Create item
            item = zot.create_items([item_data])
            
            # Check if result is a dictionary with 'successful' field
            item_key = None
            if isinstance(item, dict) and 'successful' in item:
                successful_items = item['successful']
                if successful_items and isinstance(successful_items, dict):
                    # Get the first successful item
                    first_key = next(iter(successful_items))
                    first_item = successful_items[first_key]
                    if isinstance(first_item, dict) and 'key' in first_item:
                        item_key = first_item['key']
            elif isinstance(item, list) and len(item) > 0:
                # Handle case where result is a list
                if isinstance(item[0], dict) and 'key' in item[0]:
                    item_key = item[0]['key']
            
            if not item_key:
                return {"error": f"Failed to create item using pyzotero, result: {item}"}

            # Add to specified collection
            collection_id = get_collection_id(zot, collection)
            
            if not collection_id:
                # Create collection if it doesn't exist
                collection_id = create_collection(zot, collection)
            
            added_to_collection = False
            if collection_id:
                added_to_collection = add_to_collection(zot, item_key, collection_id)
            
            return {
                "success": True,
                "item_id": item_key,
                "added_to_collection": added_to_collection
            }
        except Exception as e:
            return {"error": f"Error using pyzotero: {str(e)}"}
    
    # Continue with existing direct API calls if pyzotero is not used or not available
    
    # Check for duplicate
    existing_items = find_duplicate(paper_info, zotero_api_key, zotero_library_id, zotero_library_type)
    if existing_items:
        # Already exists, try to add to the collection if not already there
        if collection and Zotero is not None:
            zot = Zotero(zotero_api_key, zotero_library_id, zotero_library_type == "group")
            # Get the first existing item
            if isinstance(existing_items, list) and len(existing_items) > 0:
                # Get item key from the first existing item
                if 'key' in existing_items[0]:
                    item_key = existing_items[0]['key']
                    # Get collection ID
                    coll_id = get_collection_id(zot, collection)
                    if not coll_id:
                        coll_id = create_collection(zot, collection)
                    if coll_id:
                        add_to_collection(zot, item_key, coll_id)
                        return {
                            "success": True,
                            "item_id": item_key,
                            "added_to_collection": True,
                            "message": "Paper already existed, added to collection"
                        }
        return {"error": "Paper already exists in Zotero library"}
    
    # Create item in Zotero
    item_result = create_item(paper_info, zotero_api_key, zotero_library_id, zotero_library_type)

    # Handle different response formats
    added_to_collection = False
    if isinstance(item_result, dict):
        # Check if response has "successful" field (newer Zotero API format)
        if "successful" in item_result:
            successful_items = item_result["successful"]
            if successful_items:
                # Get the first successful item
                first_item_key = list(successful_items.keys())[0]
                item_key = successful_items[first_item_key].get("key")
                if item_key:
                    # Try to add to the specified collection if Zotero is available
                    if collection and Zotero is not None:
                        zot = Zotero(zotero_api_key, zotero_library_id, zotero_library_type == "group")
                        coll_id = get_collection_id(zot, collection)
                        if not coll_id:
                            coll_id = create_collection(zot, collection)
                        if coll_id:
                            added_to_collection = add_to_collection(zot, item_key, coll_id)
                    return {
                        "success": True,
                        "item_id": item_key,
                        "added_to_collection": added_to_collection
                    }
        # Check if response has "error" field
        elif "error" in item_result:
            return {"error": f"Failed to create item: {item_result['error']}"}
    elif isinstance(item_result, list) and len(item_result) > 0:
        # Older Zotero API format
        item_key = item_result[0].get("key")
        if item_key:
            # Try to add to the specified collection if Zotero is available
            if collection and Zotero is not None:
                zot = Zotero(zotero_api_key, zotero_library_id, zotero_library_type == "group")
                coll_id = get_collection_id(zot, collection)
                if not coll_id:
                    coll_id = create_collection(zot, collection)
                if coll_id:
                    added_to_collection = add_to_collection(zot, item_key, coll_id)
            return {
                "success": True,
                "item_id": item_key,
                "added_to_collection": added_to_collection
            }

    return {"error": "Failed to create item: unknown error"}

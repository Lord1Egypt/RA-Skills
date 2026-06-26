#!/usr/bin/env python3
"""
Arxiv-Zotero-Obsidian Helper Script

This script provides utility functions for the arxiv-zotero-obsidian skill.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional

# Configuration
DEFAULT_CONFIG = {
    "zotero_api_key": os.environ.get("ZOTERO_API_KEY", ""),
    "zotero_user_id": os.environ.get("ZOTERO_USER_ID", ""),
    "zotero_collection_key": os.environ.get("ZOTERO_COLLECTION_KEY", "U4PZ3XNP"),
    "obsidian_vault_path": os.environ.get("OBSIDIAN_VAULT_PATH", ""),
    "obsidian_folder": os.environ.get("OBSIDIAN_FOLDER", "DailyArXiv"),
    "arxiv_base_url": "https://arxiv.drqyq.com",
    "category": "PTA",
}


def get_arxiv_metadata(arxiv_id: str) -> Dict:
    """Fetch paper metadata from arXiv API."""
    import requests
    
    url = f"https://export.arxiv.org/api/query?id_list={arxiv_id}"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.content)
        ns = {'a': 'http://www.w3.org/2005/Atom'}
        entry = root.find('a:entry', ns)
        
        if entry is None:
            return {}
        
        title = entry.find('a:title', ns).text.replace('\n', ' ').strip()
        summary = entry.find('a:summary', ns).text.replace('\n', ' ').strip()
        published = entry.find('a:published', ns).text[:10]
        
        authors = []
        for a in entry.findall('a:author', ns):
            name = a.find('a:name', ns).text
            parts = name.split()
            if len(parts) >= 2:
                authors.append({
                    'firstName': parts[0],
                    'lastName': ' '.join(parts[1:]),
                    'creatorType': 'author'
                })
        
        return {
            'title': title,
            'summary': summary,
            'published': published,
            'authors': authors,
            'arxiv_id': arxiv_id,
            'doi': f"10.48550/arXiv.{arxiv_id}",
            'url': f"https://arxiv.org/abs/{arxiv_id}",
            'pdf_url': f"https://arxiv.org/pdf/{arxiv_id}.pdf",
        }
    except Exception as e:
        print(f"Error fetching metadata for {arxiv_id}: {e}")
        return {}


def add_to_zotero(paper: Dict, api_key: str, user_id: str, collection_key: str) -> bool:
    """Add paper to Zotero."""
    import requests
    
    url = f"https://api.zotero.org/users/{user_id}/items"
    headers = {
        "Zotero-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    item = {
        "itemType": "preprint",
        "title": paper['title'],
        "creators": paper['authors'],
        "abstractNote": paper['summary'],
        "url": paper['url'],
        "repository": "arXiv",
        "archiveID": f"arXiv:{paper['arxiv_id']}",
        "date": paper['published'],
        "DOI": paper['doi'],
        "collections": [collection_key]
    }
    
    try:
        response = requests.post(url, headers=headers, json=[item], timeout=30)
        if response.status_code == 200:
            item_data = response.json()
            if 'successful' in item_data:
                item_key = item_data['successful']['0']['key']
                add_pdf_attachment(paper['arxiv_id'], item_key, api_key, user_id)
            return True
    except Exception as e:
        print(f"Error adding to Zotero: {e}")
    
    return False


def add_pdf_attachment(arxiv_id: str, item_key: str, api_key: str, user_id: str) -> bool:
    """Add PDF link as attachment to Zotero item."""
    import requests
    
    url = f"https://api.zotero.org/users/{user_id}/items"
    headers = {
        "Zotero-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    attachment = {
        "itemType": "attachment",
        "linkMode": "linked_url",
        "title": "PDF",
        "url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
        "parentItem": item_key
    }
    
    try:
        response = requests.post(url, headers=headers, json=[attachment], timeout=30)
        return response.status_code == 200
    except:
        return False


def write_obsidian_note(paper: Dict, vault_path: str, folder: str, notes: str) -> str:
    """Write reading notes to Obsidian."""
    import os
    
    folder_path = os.path.join(vault_path, folder)
    os.makedirs(folder_path, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}-arXiv-{paper['arxiv_id']}.md"
    file_path = os.path.join(folder_path, filename)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(notes)
    
    return file_path


if __name__ == "__main__":
    print("Arxiv-Zotero-Obsidian Helper Script")
    print("=" * 40)
    print(f"Default config: {json.dumps(DEFAULT_CONFIG, indent=2)}")

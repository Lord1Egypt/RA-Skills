#!/usr/bin/env python3
"""
EPO Data Mapper - Deterministic EPO API data fetching

This script handles EPO API authentication and data collection.
It is deterministic - same inputs always produce same outputs.
The analysis and interpretation should be done by LLM agents.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
import base64
import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Any

class EPODataMapper:
    """
    Maps EPO API responses to standardized patent data format.
    Deterministic - no LLM usage here, just data transformation.
    """
    
    BASE_URL = "https://ops.epo.org/3.2"
    
    def __init__(self, consumer_key: str = None, secret_key: str = None):
        """Initialize with EPO API credentials from environment or parameters."""
        self.consumer_key = consumer_key or os.environ.get('EPO_CONSUMER_KEY')
        self.secret_key = secret_key or os.environ.get('EPO_SECRET_KEY')
        self.access_token = None
        
        if not self.consumer_key or not self.secret_key:
            raise ValueError("EPO API credentials not configured. Set EPO_CONSUMER_KEY and EPO_SECRET_KEY environment variables.")
    
    def _authenticate(self) -> str:
        """Authenticate with EPO API using OAuth2."""
        if self.access_token:
            return self.access_token
            
        auth_string = base64.b64encode(f"{self.consumer_key}:{self.secret_key}".encode()).decode()
        
        headers = {
            'Authorization': f'Basic {auth_string}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {'grant_type': 'client_credentials'}
        
        try:
            response = requests.post(
                f'{self.BASE_URL}/auth/accesstoken',
                headers=headers,
                data=data,
                timeout=30
            )
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data.get('access_token')
            
            if not self.access_token:
                raise ValueError("No access token in response")
                
            return self.access_token
            
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            raise
    
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict:
        """Make authenticated request to EPO API."""
        token = self._authenticate()
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json'
        }
        
        try:
            response = requests.get(
                f'{self.BASE_URL}/{endpoint}',
                headers=headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"❌ API request failed: {e}")
            raise
    
    def fetch_patents(self, query: str, range_start: int = 1, range_end: int = 10) -> List[Dict]:
        """
        Fetch patents from EPO API.
        
        Args:
            query: Search query (e.g., "pa=IBM", "ti=CNC")
            range_start: Start of result range (1-100)
            range_end: End of result range (1-100)
            
        Returns:
            List of patent dictionaries with standardized fields
        """
        print(f"🔍 Fetching EPO patents: {query} (range {range_start}-{range_end})")
        
        params = {
            'q': query,
            'Range': f'{range_start}-{range_end}'
        }
        
        try:
            data = self._make_request('rest-services/published-data/search/biblio', params)
            
            patents = self._parse_search_results(data)
            print(f"✅ Fetched {len(patents)} patents from EPO")
            
            return patents
            
        except Exception as e:
            print(f"❌ Failed to fetch patents: {e}")
            return []
    
    def _parse_search_results(self, data: Dict) -> List[Dict]:
        """Parse EPO search results into standardized format."""
        patents = []
        
        try:
            # Navigate to search results
            search_results = data.get('ops:world-patent-data', {}).get('ops:biblio-search', {}).get('ops:search-result', {})
            
            if not search_results:
                print("⚠️ No search results found")
                return patents
            
            # Handle the actual structure: exchange-documents is a list
            exchange_docs_list = search_results.get('exchange-documents', [])
            if not exchange_docs_list:
                print("⚠️ No exchange documents found")
                return patents
            
            # Process each exchange-documents item
            for exchange_docs_item in exchange_docs_list:
                # Each item has an 'exchange-document' key
                documents = exchange_docs_item.get('exchange-document', [])
                if not isinstance(documents, list):
                    documents = [documents]
                
                for doc in documents:
                    patent = self._parse_single_patent(doc)
                    if patent:
                        patents.append(patent)
            
            return patents
            
        except Exception as e:
            print(f"⚠️ Error parsing results: {e}")
            import traceback
            traceback.print_exc()
            return patents
    
    def _parse_single_patent(self, doc: Dict) -> Dict:
        """Parse a single patent document from EPO response."""
        try:
            biblio = doc.get('bibliographic-data', {})
            
            # Get publication reference
            pub_ref = biblio.get('publication-reference', {})
            document_ids = pub_ref.get('document-id', [])
            
            # Initialize variables
            patent_id = 'Unknown'
            kind_code = ''
            country_code = ''
            pub_date = 'Unknown'
            
            if isinstance(document_ids, list) and len(document_ids) > 0:
                # Look for epodoc type first (formatted number like US12586605)
                epodoc_doc = None
                docdb_doc = None
                
                for doc_id in document_ids:
                    doc_type = doc_id.get('@document-id-type', '')
                    
                    if doc_type == 'epodoc':
                        epodoc_doc = doc_id
                    elif doc_type == 'docdb':
                        docdb_doc = doc_id
                
                # Extract from epodoc if available
                if epodoc_doc:
                    doc_number = epodoc_doc.get('doc-number', {})
                    if isinstance(doc_number, dict):
                        patent_id = doc_number.get('$', 'Unknown')
                    else:
                        patent_id = str(doc_number)
                    
                    # Get date from epodoc
                    date_data = epodoc_doc.get('date', {})
                    if isinstance(date_data, dict):
                        pub_date = date_data.get('$', 'Unknown')
                    else:
                        pub_date = str(date_data)
                
                # Extract kind code from docdb if available
                if docdb_doc:
                    kind = docdb_doc.get('kind', {})
                    if isinstance(kind, dict):
                        kind_code = kind.get('$', '')
                    else:
                        kind_code = str(kind)
                    
                    # Get country code from docdb
                    country = docdb_doc.get('country', {})
                    if isinstance(country, dict):
                        country_code = country.get('$', '')
                    else:
                        country_code = str(country)
                    
                    # If we didn't get patent_id from epodoc, try docdb
                    if patent_id == 'Unknown' or patent_id == '':
                        doc_number = docdb_doc.get('doc-number', {})
                        if isinstance(doc_number, dict):
                            base_number = doc_number.get('$', '')
                            if base_number and country_code:
                                patent_id = f"{country_code}{base_number}"
                
                # Add kind code to patent_id if we have it
                if patent_id != 'Unknown' and kind_code:
                    patent_id = f"{patent_id}{kind_code}"
                
                # If still no patent_id, fallback to first document
                if patent_id == 'Unknown' or patent_id == '':
                    doc_id = document_ids[0]
                    doc_number = doc_id.get('doc-number', {})
                    if isinstance(doc_number, dict):
                        patent_id = doc_number.get('$', 'Unknown')
                    else:
                        patent_id = str(doc_number)
            else:
                patent_id = 'Unknown'
            
            # Get title
            titles = biblio.get('invention-title', [])
            title = self._get_text_from_list(titles, 'Unknown Title')
            
            # Get applicants (companies)
            applicants_data = biblio.get('parties', {}).get('applicants', {}).get('applicant', [])
            if not isinstance(applicants_data, list):
                applicants_data = [applicants_data]
            
            companies = []
            for applicant in applicants_data:
                # Try different possible structures
                applicant_name = applicant.get('applicant-name', {})
                name_data = applicant_name.get('name', {})
                name = name_data.get('$', '')
                
                if not name:
                    # Try addressbook structure
                    addressbook = applicant.get('addressbook', {})
                    name = addressbook.get('name', '')
                
                if name and name != 'Unknown':
                    companies.append(name)
            
            company = ', '.join(companies) if companies else 'Unknown'
            
            # Get inventors
            inventors_data = biblio.get('parties', {}).get('inventors', {}).get('inventor', [])
            if not isinstance(inventors_data, list):
                inventors_data = [inventors_data]
            
            inventors = []
            for inventor in inventors_data:
                addressbook = inventor.get('addressbook', {})
                name = addressbook.get('name', '')
                if name:
                    inventors.append(name)
            
            inventor = ', '.join(inventors) if inventors else 'Unknown'
            
            # Get abstract
            abstracts = doc.get('abstract', [])
            abstract = self._get_text_from_list(abstracts, '')
            # Truncate if too long for database
            if len(abstract) > 10000:
                abstract = abstract[:10000]
            
            # Build patent data
            patent_data = {
                'patent_id': patent_id,
                'title': title,
                'inventor': inventor,
                'company': company,
                'filing_date': pub_date,
                'publication_date': pub_date,
                'abstract': abstract,
                'category': '',  # To be determined by LLM analysis
                'technology_area': '',
                'secondary_effects': '',
                'image_url': f"https://worldwide.espacenet.com/patent/search?q=pn%3D{patent_id}",
                'created_at': datetime.now().isoformat()
            }
            
            return patent_data
            
        except Exception as e:
            print(f"⚠️ Error parsing patent: {e}")
            return None
    
    def _get_text_from_list(self, items, default=''):
        """Extract text from a list of language variants."""
        if not items:
            return default
        
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    text = item.get('$', '')
                    lang = item.get('@lang', '')
                    if text and (lang == 'en' or not lang):
                        return text
                elif isinstance(item, str):
                    return item
            return items[0] if items else default
        elif isinstance(items, dict):
            return items.get('$', default)
        else:
            return str(items) if items else default


def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python3 epo_data_mapper.py '<query>' [range_start] [range_end]")
        print("Example: python3 epo_data_mapper.py 'pa=IBM' 1 5")
        sys.exit(1)
    
    query = sys.argv[1]
    range_start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    range_end = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    
    try:
        mapper = EPODataMapper()
        patents = mapper.fetch_patents(query, range_start, range_end)
        
        # Save to database
        from database_manager import DatabaseManager
        db = DatabaseManager()
        
        saved_count = 0
        for patent in patents:
            if db.save_patent(patent):
                saved_count += 1
        
        print(f"\n✅ Retrieved {len(patents)} patents, saved {saved_count} to database")
        print(f"📊 Total patents in database: {db.get_patent_count()}")
        
        # Show sample
        for i, patent in enumerate(patents[:3], 1):
            print(f"\n{i}. {patent['patent_id']}: {patent['title'][:50]}...")
            print(f"   Company: {patent['company'][:40]}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

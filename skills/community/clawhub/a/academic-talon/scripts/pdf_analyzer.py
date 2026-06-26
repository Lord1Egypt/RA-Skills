import os
import requests
import hashlib
from typing import Optional, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print(f"Warning: .env file not found at {dotenv_path}")

# Cache directory
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".cache")
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# PDF directory
PDF_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "pdfs")
if not os.path.exists(PDF_DIR):
    os.makedirs(PDF_DIR)


def check_grobid_status() -> bool:
    """Check if Grobid service is running"""
    try:
        # Get GROBID API URL from environment variable, default to http://localhost:8070/api
        grobid_api_url = os.getenv("GROBID_API_URL", "http://localhost:8070/api")
        response = requests.get(f"{grobid_api_url}/isalive", timeout=10)
        return response.status_code == 200 and response.text == "true"
    except Exception:
        return False


def generate_bibtex_citation_key(paper_info: Dict) -> str:
    """Generate a bibtex citation key from paper information
    
    Args:
        paper_info: Dictionary containing paper information
        
    Returns:
        Bibtex citation key in the format "lastnameYearTitle"
    """
    # Get first author's last name
    authors = paper_info.get('authors', [])
    if authors:
        first_author = authors[0]
        # Check if already in "Lastname, Firstname" format (from Grobid BibTeX)
        if ',' in first_author:
            last_name = first_author.split(',')[0].strip().lower()
        else:
            # Split into words, take last part as last name
            name_parts = first_author.split()
            last_name = name_parts[-1].lower() if name_parts else "unknown"
    else:
        last_name = "unknown"
    
    # Get year
    year = paper_info.get('year', '')
    # Convert to string if it's an integer
    if isinstance(year, int):
        year = str(year)
    # Take first 4 characters in case of full date
    year = year[:4]
    if not year:
        year = ""
    
    # Get title and extract first few words
    title = paper_info.get('title', '')
    if title:
        # Remove special characters and split into words
        import re
        title_words = re.findall(r'\b\w+\b', title.lower())
        # Take first 2 words
        title_part = "".join(title_words[:2]) if title_words else ""
    else:
        title_part = ""
    
    # Combine parts
    citation_key = f"{last_name}{year}{title_part}"

    # Remove any non-alphanumeric characters
    citation_key = re.sub(r'[^a-zA-Z0-9]', '', citation_key)

    # If citation key is empty, generate a fallback
    if not citation_key or citation_key == "unknown":
        # If we have arxiv_id, use that
        if 'arxiv_id' in paper_info and paper_info['arxiv_id']:
            arxiv_id = paper_info['arxiv_id']
            clean_axid = arxiv_id.replace('arXiv:', '').replace('arXiv', '').split('/')[-1].split('[')[0].strip()
            if clean_axid:
                return f"arxiv{clean_axid}"
        # Fallback to unknown with hash
        import hashlib
        title = paper_info.get('title', '')
        if title:
            hash_obj = hashlib.md5(title.encode())
            hash_short = hash_obj.hexdigest()[:8]
            return f"paper{hash_short}"
        return "unknown"

    return citation_key

def download_pdf(url: str, filename: str = None, save_dir: str = None, paper_info: Dict = None) -> Optional[str]:
    """Download PDF from URL to local file
    
    Args:
        url: URL of the PDF file
        filename: Optional filename to save the PDF as
        save_dir: Optional directory to save the PDF in
        paper_info: Optional paper information for generating citation key
        
    Returns:
        Path to the downloaded PDF file, or None if download failed
    """
    try:
        # Determine save directory
        if save_dir:
            # Use specified directory
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            target_dir = save_dir
        else:
            # Use default PDF directory
            target_dir = PDF_DIR
        
        # Generate filename if not provided
        if not filename:
            if paper_info:
                # Generate bibtex citation key
                citation_key = generate_bibtex_citation_key(paper_info)
                filename = f"{citation_key}.pdf"
            else:
                # Extract filename from URL
                filename = os.path.basename(url)
                if not filename.endswith('.pdf'):
                    filename = f"{filename}.pdf"

        # Sanitize filename to prevent path traversal
        # Remove any directory components, keep only the filename
        filename = os.path.basename(filename)
        # Remove any non-alphanumeric except . - _
        import re
        filename = re.sub(r'[^\w\.\-]', '_', filename)
        # Ensure it still ends with .pdf
        if not filename.endswith('.pdf'):
            filename = f"{filename}.pdf"

        # Full path to save the PDF
        pdf_path = os.path.abspath(os.path.join(target_dir, filename))
        # Verify the final path is still within target directory (sandboxing)
        target_dir_abs = os.path.abspath(target_dir)
        if not pdf_path.startswith(target_dir_abs + os.sep):
            print(f"Error: filename escapes target directory sandbox: {filename}")
            return None
        
        # Download PDF
        print(f"Downloading PDF from {url} to {pdf_path}")
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Save PDF to file
        with open(pdf_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"PDF downloaded successfully: {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"Error downloading PDF: {e}")
        return None


def get_pdf_hash(pdf_path: str) -> str:
    """Generate a hash for the PDF file"""
    hasher = hashlib.md5()
    with open(pdf_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


def get_xml_cache_file(pdf_path: str, endpoint: str) -> str:
    """Get the XML cache file path for the PDF"""
    pdf_hash = get_pdf_hash(pdf_path)
    return os.path.join(CACHE_DIR, f"{pdf_hash}_{endpoint.replace('/', '_')}.xml")


def save_xml_response(pdf_path: str, endpoint: str, xml_response: str):
    """Save XML response to cache"""
    xml_cache_file = get_xml_cache_file(pdf_path, endpoint)
    try:
        with open(xml_cache_file, 'w', encoding='utf-8') as f:
            f.write(xml_response)
        print(f"Saved XML response: {xml_cache_file}")
    except Exception as e:
        print(f"Error saving XML response: {e}")


def load_xml_response(pdf_path: str, endpoint: str) -> Optional[str]:
    """Load XML response from cache"""
    xml_cache_file = get_xml_cache_file(pdf_path, endpoint)
    if os.path.exists(xml_cache_file):
        try:
            with open(xml_cache_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading XML response: {e}")
    return None


def process_pdf(pdf_input: str, endpoint: str = "processFulltextDocument") -> str:
    """Process PDF with Grobid and return XML response
    
    Args:
        pdf_input: Path to local PDF file or URL to PDF
        endpoint: Grobid API endpoint to use
        
    Returns:
        XML response from Grobid
    """
    # Check if Grobid is running
    if not check_grobid_status():
        error_message = "Grobid service is not running. Please start Grobid first."
        print(error_message)
        return error_message
    
    # Check if input is a URL
    if pdf_input.startswith('http://') or pdf_input.startswith('https://'):
        # Download PDF from URL
        pdf_path = download_pdf(pdf_input)
        if not pdf_path:
            return ""
    else:
        # Use local PDF path
        pdf_path = pdf_input
    
    # Check if XML response is already cached
    xml_response = load_xml_response(pdf_path, endpoint)
    if xml_response:
        print(f"Loaded XML response from cache: {get_xml_cache_file(pdf_path, endpoint)}")
        return xml_response
    
    # Get GROBID API URL from environment variable, default to http://localhost:8070/api
    grobid_api_url = os.getenv("GROBID_API_URL", "http://localhost:8070/api")
    grobid_url = f"{grobid_api_url}/{endpoint}"
    
    print(f"Processing PDF: {pdf_path}")
    print(f"Grobid URL: {grobid_url}")
    
    try:
        # Check if PDF file exists
        if not os.path.exists(pdf_path):
            print(f"PDF file not found: {pdf_path}")
            return ""
        
        # Check if PDF file is readable
        if not os.access(pdf_path, os.R_OK):
            print(f"PDF file not readable: {pdf_path}")
            return ""
        
        # Send PDF to Grobid for processing with consolidate parameters
        print("Sending PDF to Grobid...")
        with open(pdf_path, 'rb') as f:
            files = {'input': f}
            data = {
                'consolidateHeader': '1',
                'consolidateCitations': '1'
            }
            # Set timeout to 5 minutes
            response = requests.post(grobid_url, files=files, data=data, timeout=300)
        
        print(f"Grobid response status code: {response.status_code}")
        
        if response.status_code == 200:
            print("Grobid API call successful")
            # Get XML response
            xml_response = response.text
            
            # Save XML response
            save_xml_response(pdf_path, endpoint, xml_response)
            
            # Print first 500 characters of XML response for debugging
            print(f"XML response (first 500 chars): {xml_response[:500]}...")
            
            return xml_response
        else:
            print(f"Grobid API error: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.exceptions.Timeout:
        print("Grobid API request timed out")
    except requests.exceptions.ConnectionError:
        print("Grobid API connection error - is Grobid running?")
    except Exception as e:
        print(f"Error processing PDF with Grobid: {e}")
        import traceback
        print(traceback.format_exc())
    
    return ""


def parse_grobid_header_to_bibtex(grobid_response: str) -> str:
    """Parse Grobid response into BibTeX format

    Args:
        grobid_response: Response from Grobid processHeaderDocument (could be TEI XML or BibTeX)

    Returns:
        BibTeX string
    """
    # If Grobid is configured to return BibTeX directly, parse it and reformat
    # according to our standard format
    if grobid_response.strip().startswith('@'):
        # Try to extract information from the existing BibTeX
        import re

        # Extract fields with regex
        text = grobid_response

        # Extract authors
        authors_match = re.search(r'author\s*=\s*\{([^}]+)\}', text, re.DOTALL)
        authors_str = authors_match.group(1) if authors_match else ""
        # Split by " and " - BibTeX author separation
        import re
        authors = []
        if authors_str:
            authors = re.split(r'\s+and\s+', authors_str)
            # Clean up each author
            authors = [a.strip() for a in authors if a.strip()]

        # Extract title
        title_match = re.search(r'title\s*=\s*\{([^}]+)\}', text, re.DOTALL)
        title = title_match.group(1).strip() if title_match else None

        # Extract year
        year_match = re.search(r'year\s*=\s*\{([^}]+)\}', text)
        year = year_match.group(1).strip() if year_match else None

        # Extract eprint (arXiv ID)
        arxiv_match = re.search(r'eprint\s*=\s*\{([^}]+)\}', text)
        arxiv_id = arxiv_match.group(1).strip() if arxiv_match else None

        # Extract doi
        doi_match = re.search(r'doi\s*=\s*\{([^}]+)\}', text)
        doi = doi_match.group(1).strip() if doi_match else None

        # Extract abstract
        abstract_match = re.search(r'abstract\s*=\s*\{([^}]+)\}', text, re.DOTALL)
        abstract = abstract_match.group(1).strip() if abstract_match else None

        # Determine entry type
        entry_type = "misc"
        journal = None
        conference = None

        if arxiv_id:
            entry_type = "article"  # arXiv preprint
        elif "journal" in text:
            entry_type = "article"
            journal_match = re.search(r'journal\s*=\s*\{([^}]+)\}', text)
            journal = journal_match.group(1).strip() if journal_match else None
        elif "booktitle" in text:
            entry_type = "inproceedings"
            conference_match = re.search(r'booktitle\s*=\s*\{([^}]+)\}', text)
            conference = conference_match.group(1).strip() if conference_match else None

        # Generate proper citation key
        paper_info = {
            'authors': authors,
            'year': year,
            'title': title,
            'arxiv_id': arxiv_id
        }
        citation_key = generate_bibtex_citation_key(paper_info)

        # Format authors in BibTeX format
        # Authors from Grobid BibTeX are already in "Lastname, Firstname" format, use directly
        bibtex_author_str = ' and '.join(authors)

        # Generate BibTeX in our standard format
        bibtex_lines = []
        bibtex_lines.append(f"@{entry_type}{{{citation_key},")
        if bibtex_author_str:
            bibtex_lines.append(f"  author = {{{bibtex_author_str}}},")
        if title:
            bibtex_lines.append(f"  title = {{{title}}},")
        if journal:
            bibtex_lines.append(f"  journal = {{{journal}}},")
        if conference:
            bibtex_lines.append(f"  booktitle = {{{conference}}},")
        if year:
            bibtex_lines.append(f"  year = {{{year}}},")
        # Handle arXiv preprint following standard format
        if arxiv_id and not journal and not conference:
            clean_arxiv_id = arxiv_id.replace('arXiv:', '').replace('arXiv', '').split('[')[0].strip()
            if clean_arxiv_id:
                bibtex_lines.append(f"  journal = {{arXiv preprint {clean_arxiv_id}}},")
        if doi:
            bibtex_lines.append(f"  doi = {{{doi}}},")
        if abstract:
            if len(abstract) > 1000:
                abstract = abstract[:1000] + '...'
            bibtex_lines.append(f"  abstract = {{{abstract}}},")
        bibtex_lines.append("}")

        return '\n'.join(bibtex_lines)

    try:
        import xml.etree.ElementTree as ET

        # Parse XML
        root = ET.fromstring(grobid_response)

        # Extract header element (TEI:teiHeader -> fileDesc -> titleStmt)
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        title_stmt = root.find('.//tei:teiHeader//tei:fileDesc//tei:titleStmt', ns)
        publication_stmt = root.find('.//tei:teiHeader//tei:fileDesc//tei:publicationStmt', ns)
        source_desc = root.find('.//tei:teiHeader//tei:fileDesc//tei:sourceDesc', ns)

        # Extract title
        title = None
        if title_stmt is not None:
            title_elem = title_stmt.find('.//tei:title', ns)
            if title_elem is not None and title_elem.text:
                title = title_elem.text.strip()

        # Extract authors
        authors = []
        if title_stmt is not None:
            author_elems = title_stmt.findall('.//tei:author', ns)
            for author in author_elems:
                forename = author.find('.//tei:forename', ns)
                surname = author.find('.//tei:surname', ns)
                name_parts = []
                if forename is not None and forename.text:
                    name_parts.append(forename.text.strip())
                if surname is not None and surname.text:
                    name_parts.append(surname.text.strip())
                full_name = ' '.join(name_parts)
                if full_name:
                    authors.append(full_name)

        # Extract date
        year = None
        month = None
        day = None
        # Look for publication date
        date_elem = root.find('.//tei:date', ns)
        if date_elem is not None:
            if 'when' in date_elem.attrib:
                date_str = date_elem.attrib['when']
                parts = date_str.split('-')
                if len(parts) >= 1:
                    year = parts[0]
                if len(parts) >= 2:
                    month = parts[1]
                if len(parts) >= 3:
                    day = parts[2]

        # Extract DOI
        doi = None
        idno_elems = root.findall('.//tei:idno', ns)
        for idno in idno_elems:
            if idno.text and '10.' in idno.text:
                doi = idno.text.strip()
                break

        # Extract arXiv ID
        arxiv_id = None
        for idno in idno_elems:
            if idno.text and ('arxiv' in idno.text.lower() or 'arXiv' in idno.text):
                arxiv_id = idno.text.strip()
                break

        # Extract publication information (publisher/journal/conference)
        publication = None
        publisher = None
        journal = None
        conference = None

        if publication_stmt is not None:
            # Try to find publisher
            publisher_elem = publication_stmt.find('.//tei:publisher', ns)
            if publisher_elem is not None and publisher_elem.text:
                publisher = publisher_elem.text.strip()

            # Try to find journal name
            journal_elem = publication_stmt.find('.//tei:journal//tei:title', ns)
            if journal_elem is not None and journal_elem.text:
                journal = journal_elem.text.strip()

            # Try to find conference name (look in publicationStmt and notes)
            conference_elem = publication_stmt.find('.//tei:conference//tei:title', ns)
            if conference_elem is not None and conference_elem.text:
                conference = conference_elem.text.strip()

            # Check notes for arXiv information
            notesStmt = root.find('.//tei:notesStmt', ns)
            if notesStmt is not None:
                for note in notesStmt.findall('.//tei:note', ns):
                    if note.text and ('arxiv' in note.text.lower() or 'arXiv' in note.text):
                        publication = note.text.strip()
                        break

        # Determine entry type based on publication
        entry_type = "misc"
        if journal:
            entry_type = "article"  # journal article
        elif conference:
            entry_type = "inproceedings"  # conference paper
        elif publisher and "arXiv" in publisher:
            entry_type = "article"  # arXiv preprint
        elif arxiv_id:
            entry_type = "article"  # arXiv preprint

        # Generate proper citation key: lastnameYearTitle
        paper_info = {
            'authors': authors,
            'year': year,
            'title': title
        }
        citation_key = generate_bibtex_citation_key(paper_info)
        if not citation_key or citation_key == "unknown":
            citation_key = "-1"

        # Build BibTeX
        # Format authors: "Lastname, Firstname and Lastname2, Firstname2"
        bibtex_authors = []
        for author in authors:
            parts = author.strip().split()
            if len(parts) >= 2:
                # Assume last part is last name
                lastname = parts[-1]
                firstnames = ' '.join(parts[:-1])
                bibtex_authors.append(f"{lastname}, {firstnames}")
            else:
                bibtex_authors.append(author)
        bibtex_author_str = ' and '.join(bibtex_authors)

        # Generate BibTeX - clean format matching your examples
        # Keep only essential fields, minimal and clean for publication
        bibtex_lines = []
        bibtex_lines.append(f"@{entry_type}{{{citation_key},")
        if bibtex_author_str:
            bibtex_lines.append(f"  author = {{{bibtex_author_str}}},")
        if title:
            bibtex_lines.append(f"  title = {{{title}}},")
        if journal:
            bibtex_lines.append(f"  journal = {{{journal}}},")
        if conference:
            bibtex_lines.append(f"  booktitle = {{{conference}}},")
        if year:
            bibtex_lines.append(f"  year = {{{year}}},")
        # Only include month for conference papers
        if month and entry_type == "inproceedings":
            bibtex_lines.append(f"  month = {{{month}}},")
        # Handle arXiv preprint following your example format
        if arxiv_id and not journal and not conference:
            clean_arxiv_id = arxiv_id.replace('arXiv:', '').replace('arXiv', '').split('[')[0].strip()
            if clean_arxiv_id:
                # Format: journal = {arXiv preprint arXiv:xxxx.xxxxx}
                bibtex_lines.append(f"  journal = {{arXiv preprint {clean_arxiv_id}}},")
        # Only include DOI if available
        if doi:
            bibtex_lines.append(f"  doi = {{{doi}}},")

        # Extract abstract - optional but useful for annotation
        abstract_elem = root.find('.//tei:abstract', ns)
        if abstract_elem is not None:
            # Get all text content
            abstract_text = ''
            for p in abstract_elem.findall('.//tei:p', ns):
                if p.text:
                    abstract_text += p.text.strip() + ' '
            if abstract_text:
                # Truncate if too long
                if len(abstract_text) > 1000:
                    abstract_text = abstract_text[:1000] + '...'
                bibtex_lines.append(f"  abstract = {{{abstract_text.strip()}}},")

        bibtex_lines.append("}")

        return '\n'.join(bibtex_lines)

    except Exception as e:
        print(f"Error parsing Grobid response to BibTeX: {e}")
        import traceback
        traceback.print_exc()
        # Return original response if parsing fails
        return grobid_response


def analyze_pdf_header(pdf_input: str) -> str:
    """Analyze PDF header and return BibTeX format

    Args:
        pdf_input: Path to local PDF file or URL to PDF

    Returns:
        BibTeX string generated from GROBID header analysis
    """
    xml_response = process_pdf(pdf_input, endpoint="processHeaderDocument")
    if not xml_response or xml_response.startswith("Error"):
        return xml_response
    # Convert XML to BibTeX
    return parse_grobid_header_to_bibtex(xml_response)


def analyze_pdf_fulltext(pdf_input: str) -> str:
    """Analyze PDF fulltext and return XML response
    
    Args:
        pdf_input: Path to local PDF file or URL to PDF
        
    Returns:
        XML response from Grobid
    """
    return process_pdf(pdf_input, endpoint="processFulltextDocument")
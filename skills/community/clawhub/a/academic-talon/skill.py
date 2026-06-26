import os
import json
from typing import Dict, List, Any
from scripts.search import search_papers
from scripts.pdf_analyzer import analyze_pdf_header, analyze_pdf_fulltext, download_pdf
from scripts.zotero_archiver import archive_paper

class AcademicTalonSkill:
    """Academic Talon Skill for searching, analyzing, and archiving academic papers"""
    
    def __init__(self):
        """Initialize the skill"""
        # Load environment variables
        from dotenv import load_dotenv
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        else:
            print(f"Warning: .env file not found at {dotenv_path}")
    
    def search_papers(self, query: str, limit: int = 10, source: str = "all", engine_weights: Dict[str, int] = None) -> List[Dict[str, Any]]:
        """Search papers from multiple sources
        
        Args:
            query: Search query
            limit: Number of results to return
            source: Search source ("all", "semantic_scholar", "arxiv", "google_scholar", "tavily")
            engine_weights: Dictionary of engine weights (only applies when source="all")
            
        Returns:
            List of paper dictionaries
        """
        try:
            papers = search_papers(query, limit, source, engine_weights=engine_weights)
            return papers
        except Exception as e:
            print(f"Error searching papers: {e}")
            return []
    
    def download_pdf(self, url: str, filename: str = None, save_dir: str = None, paper_info: Dict = None) -> str:
        """Download PDF from URL
        
        Args:
            url: URL of the PDF file
            filename: Optional filename to save the PDF as
            save_dir: Optional directory to save the PDF in (must be within the skill's pdfs directory)
            paper_info: Optional paper information for generating citation key
            
        Returns:
            Path to the downloaded PDF file
        """
        try:
            # Restrict save_dir to be within the skill's pdfs directory
            if save_dir:
                # Get the skill's pdfs directory
                skill_dir = os.path.dirname(__file__)
                pdfs_dir = os.path.join(skill_dir, "pdfs")
                # Resolve the absolute path of save_dir
                save_dir_abs = os.path.abspath(save_dir)
                # Check if save_dir is within pdfs_dir
                if not save_dir_abs.startswith(pdfs_dir):
                    print("Error: save_dir must be within the skill's pdfs directory")
                    return ""
            
            pdf_path = download_pdf(url, filename, save_dir, paper_info)
            if not pdf_path:
                return ""
            return pdf_path
        except Exception as e:
            print(f"Error downloading PDF: {e}")
            return ""
    
    def analyze_pdf(self, pdf_input: str, analysis_type: str = "header") -> str:
        """Analyze PDF file
        
        Args:
            pdf_input: URL to PDF or path to local PDF file within the skill's pdfs directory
            analysis_type: Type of analysis ("header" or "fulltext")
            
        Returns:
            Analysis result (BibTeX for header, XML for fulltext)
        """
        try:
            # Restrict pdf_input to be either a URL or within the skill's pdfs directory
            if not (pdf_input.startswith('http://') or pdf_input.startswith('https://')):
                # It's a local file path, check if it's within the skill's pdfs directory
                skill_dir = os.path.dirname(__file__)
                pdfs_dir = os.path.join(skill_dir, "pdfs")
                # Resolve the absolute path of pdf_input
                pdf_input_abs = os.path.abspath(pdf_input)
                # Check if pdf_input is within pdfs_dir
                if not pdf_input_abs.startswith(pdfs_dir):
                    print("Error: pdf_input must be a URL or within the skill's pdfs directory")
                    return "Error: pdf_input must be a URL or within the skill's pdfs directory"
            
            if analysis_type == "header":
                return analyze_pdf_header(pdf_input)
            elif analysis_type == "fulltext":
                return analyze_pdf_fulltext(pdf_input)
            else:
                return "Invalid analysis type"
        except Exception as e:
            print(f"Error analyzing PDF: {e}")
            return f"Error: {str(e)}"
    
    def archive_to_zotero(self, paper_info: Dict[str, Any], collection: str = "openclaw") -> Dict[str, Any]:
        """Archive paper to Zotero
        
        Args:
            paper_info: Dictionary containing paper information
            collection: Name of the collection to add the paper to (default: "openclaw")
            
        Returns:
            Archiving result
        """
        try:
            result = archive_paper(paper_info, use_pyzotero=True, collection=collection)
            return result
        except Exception as e:
            print(f"Error archiving to Zotero: {e}")
            return {"error": str(e)}
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the skill
        
        Args:
            input_data: Input data for the skill
            
        Returns:
            Skill output
        """
        try:
            # Get input parameters
            query = input_data.get("query", "")
            action = input_data.get("action", "search")
            limit = input_data.get("limit", 10)
            source = input_data.get("source", "all")
            
            if action == "search":
                # Search papers
                # Default engine weights: arXiv (5), Google Scholar (3), Semantic Scholar (1), Tavily (1)
                engine_weights = input_data.get("engine_weights", {
                    "arxiv": 5,
                    "google_scholar": 3,
                    "semantic_scholar": 1,
                    "tavily": 1
                })
                papers = self.search_papers(query, limit, source, engine_weights)
                return {
                    "success": True,
                    "action": "search",
                    "query": query,
                    "results": papers
                }
            
            elif action == "download":
                # Download PDF
                url = input_data.get("url", "")
                filename = input_data.get("filename", None)
                save_dir = input_data.get("save_dir", None)
                paper_info = input_data.get("paper_info", None)
                
                if not url:
                    return {
                        "success": False,
                        "error": "URL is required"
                    }
                
                pdf_path = self.download_pdf(url, filename, save_dir, paper_info)
                if not pdf_path:
                    return {
                        "success": False,
                        "error": "Failed to download PDF"
                    }
                
                return {
                    "success": True,
                    "action": "download",
                    "url": url,
                    "pdf_path": pdf_path
                }
            
            elif action == "analyze":
                # Analyze PDF
                pdf_input = input_data.get("pdf_input", "")
                analysis_type = input_data.get("analysis_type", "header")
                
                if not pdf_input:
                    return {
                        "success": False,
                        "error": "PDF input (path or URL) is required"
                    }
                
                result = self.analyze_pdf(pdf_input, analysis_type)
                return {
                    "success": True,
                    "action": "analyze",
                    "pdf_input": pdf_input,
                    "analysis_type": analysis_type,
                    "result": result
                }
            
            elif action == "archive":
                # Archive to Zotero
                paper_info = input_data.get("paper_info", {})
                collection = input_data.get("collection", "openclaw")
                
                if not paper_info:
                    return {
                        "success": False,
                        "error": "Paper information is required"
                    }
                
                result = self.archive_to_zotero(paper_info, collection=collection)
                return {
                    "success": True,
                    "action": "archive",
                    "result": result
                }
            
            else:
                return {
                    "success": False,
                    "error": "Invalid action"
                }
        
        except Exception as e:
            print(f"Error running skill: {e}")
            return {
                "success": False,
                "error": str(e)
            }

# Create skill instance
skill = AcademicTalonSkill()

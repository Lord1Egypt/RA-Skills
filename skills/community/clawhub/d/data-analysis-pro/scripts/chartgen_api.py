#!/usr/bin/env python3
"""
ChartGen API Client

Environment Variables:
    CHARTGEN_API_KEY: API key (obtain from chartgen.ai)
"""
import os
import json
import requests
from typing import Optional, Dict, Any


class ChartGenAPI:
    """ChartGen API Client"""
    
    BASE_URL = "https://chartgen.ai/api/platform_api/"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize API client
        
        Args:
            api_key: API key, if not provided, read from environment variable CHARTGEN_API_KEY
        """
        self.api_key = api_key or os.environ.get("CHARTGEN_API_KEY")
        if not self.api_key:
            raise ValueError(
                "CHARTGEN_API_KEY not set. "
                "Please set the environment variable: export CHARTGEN_API_KEY='your-api-key'"
            )
    
    def call(self, service_name: str, data: Dict[str, Any]) -> str:
        """
        Call API service
        
        Args:
            service_name: Service name (e.g., PythonDataAnalysis, DataInterpretation, EchartsVisualization)
            data: Request data
            
        Returns:
            API result text
            
        Raises:
            Exception: When API call fails
        """
        url = self.BASE_URL + service_name
        headers = {
            "Authorization": self.api_key,
            "X-Platform-Source": "openclaw",
            "Content-Type": "application/json"
        }
        
        # Add version number
        data["version"] = "1.0.0"
        
        try:
            response = requests.post(
                url, 
                headers=headers, 
                data=json.dumps(data),
                timeout=60
            )
            result = response.json()
        except requests.exceptions.Timeout:
            raise Exception("API request timeout. Please try again.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")
        except json.JSONDecodeError:
            raise Exception(
                "Invalid API response. "
                "Please check if your API key is valid or if the maximum number of calls has been reached."
            )
        
        if result.get("status") != 200:
            error_msg = result.get("message", str(result))
            raise Exception(f"API error: {error_msg}")
        
        return result.get("data", "")
    
    def analyze(self, query: str, file_path: Optional[str] = None, json_data: Optional[Any] = None) -> str:
        """
        Data Analysis
        
        Args:
            query: Analysis query statement
            file_path: Local file path (.xlsx/.xls/.csv)
            json_data: JSON data (list or dict)
            
        Returns:
            Analysis result text
        """
        data = self._prepare_input(query, file_path, json_data)
        return self.call("PythonDataAnalysis", data)
    
    def interpret(self, query: str, file_path: Optional[str] = None, json_data: Optional[Any] = None) -> str:
        """
        Data Interpretation
        
        Args:
            query: Interpretation query statement
            file_path: Local file path (.xlsx/.xls/.csv)
            json_data: JSON data (list or dict)
            
        Returns:
            Interpretation result text
        """
        data = self._prepare_input(query, file_path, json_data)
        return self.call("DataInterpretation", data)
    
    def visualize(self, query: str, file_path: Optional[str] = None, json_data: Optional[Any] = None) -> str:
        """
        Data Visualization
        
        Args:
            query: Visualization query statement
            file_path: Local file path (.xlsx/.xls/.csv)
            json_data: JSON data (list or dict)
            
        Returns:
            ECharts configuration JSON string
        """
        data = self._prepare_input(query, file_path, json_data)
        return self.call("EchartsVisualization", data)
    
    def _prepare_input(
        self, 
        query: str, 
        file_path: Optional[str] = None, 
        json_data: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Prepare input data
        
        Args:
            query: Query statement
            file_path: Local file path
            json_data: JSON data
            
        Returns:
            Prepared request data dict
        """
        import base64
        
        data = {"query": query}
        
        if file_path:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            with open(file_path, 'rb') as f:
                content = f.read()
            
            data["file_blob"] = base64.b64encode(content).decode('utf-8')
            data["file_extension"] = file_path.split('.')[-1].lower()
            
        elif json_data is not None:
            data["input_json"] = json_data
        else:
            raise ValueError("Either file_path or json_data must be provided")
        
        return data

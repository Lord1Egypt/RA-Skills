#!/usr/bin/env python3
"""
测试工具功能
"""

import pytest
import os
from unittest.mock import patch, mock_open

from src.tools.file_tools import FileTools
from src.tools.network_tools import NetworkTools


class TestFileTools:
    """测试文件工具"""
    
    def test_read_file(self):
        """测试读取文件"""
        tools = FileTools()
        with patch("builtins.open", mock_open(read_data="Hello, World!")):
            result = tools.read_file({"path": "test.txt"})
        assert result == "Hello, World!"
    
    def test_write_file(self):
        """测试写入文件"""
        tools = FileTools()
        with patch("builtins.open", mock_open()) as mock_file:
            with patch("os.makedirs"):
                result = tools.write_file({
                    "path": "test.txt",
                    "content": "Hello, World!"
                })
        assert "Successfully wrote" in result


class TestNetworkTools:
    """测试网络工具"""
    
    def test_http_request(self):
        """测试HTTP请求"""
        tools = NetworkTools()
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.headers = {}
            mock_get.return_value.text = "OK"
            
            result = tools.http_request({
                "url": "https://example.com",
                "method": "GET"
            })
        
        assert result["status"] == 200
        assert result["body"] == "OK"

#!/usr/bin/env python3
import json
import sys
import urllib.request
import urllib.error
import ssl
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from configure import get_credentials

ACCESS_KEY, SECRET_KEY = get_credentials()
BASE_URL = 'https://open.gangtise.com'

# Get token
url = BASE_URL + '/application/auth/oauth/open/loginV2'
data = {'accessKey': ACCESS_KEY, 'secretAccessKey': SECRET_KEY}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), 
                            headers={'Content-Type': 'application/json'})
context = ssl._create_unverified_context()

try:
    with urllib.request.urlopen(req, context=context) as response:
        result = json.loads(response.read().decode('utf-8'))
        if result['code'] == '000000':
            token = result['data']['accessToken']
            print('Token obtained')
            
            # Query for recent financial news
            query_url = BASE_URL + '/application/open-data/ai/search/knowledge/batch'
            # Search for various financial news sources and topics
            queries = [
                '今日财经新闻',
                'A股市场动态',
                '板块轮动',
                '原油价格',
                '中东局势',
                '算力 AI',
                '政策催化'
            ]
            
            query_data = {
                'queries': queries[:5],  # Max 5 queries
                'top': 5,
                'resourceTypes': [10, 40, 50, 60],  # Research reports, analyst views, announcements, meeting minutes
                'startTime': int((datetime.now().timestamp() - 30*24*3600) * 1000)  # Last 30 days
            }
            
            req2 = urllib.request.Request(query_url, 
                                         data=json.dumps(query_data).encode('utf-8'),
                                         headers={
                                             'Content-Type': 'application/json',
                                             'Authorization': token
                                         })
            
            with urllib.request.urlopen(req2, context=context) as response2:
                result2 = json.loads(response2.read().decode('utf-8'))
                
                if result2['code'] == '000000':
                    all_results = []
                    for query_result in result2.get('data', []):
                        for item in query_result.get('data', []):
                            all_results.append({
                                'title': item.get('title', ''),
                                'content': item.get('content', ''),
                                'time': item.get('time', 0),
                                'resourceType': item.get('resourceType', ''),
                                'company': item.get('company', ''),
                                'industry': item.get('industry', '')
                            })
                    
                    # Sort by time (newest first)
                    all_results.sort(key=lambda x: x['time'], reverse=True)
                    
                    # Print first 10 results
                    for i, item in enumerate(all_results[:10]):
                        print(f"\n--- Result {i+1} ---")
                        print(f"Title: {item['title']}")
                        if item['time']:
                            dt = datetime.fromtimestamp(item['time']/1000)
                            print(f"Time: {dt.strftime('%Y-%m-%d %H:%M')}")
                        if item['resourceType']:
                            print(f"Type: {item['resourceType']}")
                        if item['company']:
                            print(f"Company: {item['company']}")
                        if item['industry']:
                            print(f"Industry: {item['industry']}")
                        
                        # Print first 200 chars of content
                        content_preview = item['content'][:200] + '...' if len(item['content']) > 200 else item['content']
                        print(f"Preview: {content_preview}")
                else:
                    print(f"Query failed: {result2.get('msg')}")
        else:
            print(f"Auth failed: {result.get('msg')}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
#!/usr/bin/env python3
"""
Initialize baby words database
Usage: python init_database.py [child_name] [birth_date]
"""

import json
import sys
from datetime import datetime

def init_database(child_name="宝宝", birth_date="2024-04-01"):
    """Create initial database structure"""
    database = {
        "childName": child_name,
        "birthDate": birth_date,
        "currentAge": "",
        "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
        "totalWords": 0,
        "byLanguage": {
            "普通话": {
                "单字": {"count": 0, "words": []},
                "双字": {"count": 0, "words": []},
                "三字": {"count": 0, "words": []},
                "句子": {"count": 0, "words": []}
            },
            "广东话": {
                "单字": {"count": 0, "words": []},
                "双字": {"count": 0, "words": []},
                "三字": {"count": 0, "words": []},
                "句子": {"count": 0, "words": []}
            },
            "英语": {
                "单字": {"count": 0, "words": []},
                "双字": {"count": 0, "words": []},
                "三字": {"count": 0, "words": []},
                "句子": {"count": 0, "words": []}
            }
        },
        "wordRegistry": {},
        "feishuDoc": {
            "url": "",
            "docId": "",
            "createdAt": "",
            "lastSynced": ""
        }
    }
    
    return database

if __name__ == "__main__":
    child_name = sys.argv[1] if len(sys.argv) > 1 else "宝宝"
    birth_date = sys.argv[2] if len(sys.argv) > 2 else "2024-04-01"
    
    db = init_database(child_name, birth_date)
    print(json.dumps(db, ensure_ascii=False, indent=2))

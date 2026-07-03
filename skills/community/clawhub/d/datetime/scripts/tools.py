from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_datetime(
    format: str
) -> Dict[str, Any]:
    """
    Get current date and time in various formats
    
    Args:
        format: 
Available formats:
- date: 2024-12-10
- date_slash: 2024/12/10
- date_jp: 2024年12月10日
- datetime: 2024-12-10 00:54:01
- datetime_jp: 2024年12月10日 00時54分01秒
- datetime_t: 2024-12-10T00:54:01
- compact: 20241210005401
- compact_date: 20241210
- compact_time: 005401
- filename_md: 20241210005401.md
- filename_txt: 20241210005401.txt
- filename_log: 20241210005401.log
- iso: 2024-12-10T00:54:01+0900
- iso_basic: 20241210T005401+0900
- log: 2024-12-10 00:54:01.123456
- log_compact: 20241210_005401
- time: 00:54:01
- time_jp: 00時54分01秒

    
    Returns:
        
    """
    arguments = {
        "format": format
    }
    
    return call_api("1777419075044355", "get_datetime", arguments)


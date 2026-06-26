import requests
import time
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any

class StockAnnouncementPlugin:
    """
    OpenClaw Plugin for querying stock announcements from SZSE and SSE.
    """
    name = "cn_stock_announcements"
    
    def install(self, client: Any):
        """
        Register the tool with the OpenClaw client.
        Assuming client has a register_tool or similar method.
        """
        if hasattr(client, 'register_tool'):
            client.register_tool(
                name="query_stock_announcements",
                func=self.query_announcements,
                description="Query recent announcements for Chinese listed companies (SZSE & SSE) by stock code, keyword, and date range."
            )
        else:
            print(f"[{self.name}] Client does not have 'register_tool'. Manual binding required.")

    def query_announcements(
        self,
        stock_codes: Optional[List[str]] = None,
        keyword: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 10
    ) -> Dict[str, List[str]]:
        """
        Query announcements.
        :param stock_codes: List of stock codes (e.g. ['000001', '600000'])
        :param keyword: Search keyword (e.g. '年报')
        :param start_date: Start date string 'YYYY-MM-DD HH:MM:SS' or 'YYYY-MM-DD', 不传默认为近3天
        :param end_date: End date string 'YYYY-MM-DD HH:MM:SS' or 'YYYY-MM-DD', 不传默认为今天
        :param limit: Max number of results per exchange
        :return: Dict containing lists of announcements for 'SZSE' and 'SSE'
        """
        # 默认近3天
        today = datetime.now().strftime("%Y-%m-%d")
        three_days_ago = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
        start_date = start_date[:10] if start_date else three_days_ago
        end_date = end_date[:10] if end_date else today

        szse_stocks = [s for s in (stock_codes or []) if s.startswith("0") or s.startswith("3")]
        sse_stocks = [s for s in (stock_codes or []) if s.startswith("6") or s.startswith("9")]
        
        results = {"SZSE": [], "SSE": []}
        
        # Determine if we should query SZSE
        if (not stock_codes) or szse_stocks or keyword:
            szse_res = self._query_szse(szse_stocks, keyword, start_date, end_date, limit)
            results["SZSE"] = szse_res
            
        # Determine if we should query SSE
        if (not stock_codes) or sse_stocks or keyword:
            sse_res = self._query_sse(sse_stocks, keyword, start_date, end_date, limit)
            results["SSE"] = sse_res
            
        return results

    def _query_szse(self, stock_codes, keyword, start_date, end_date, limit):
        url = "http://www.szse.cn/api/disc/announcement/annList?random=" + str(time.time())
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        
        se_date = [start_date[:10] if len(start_date) > 10 else start_date, end_date[:10] if len(end_date) > 10 else end_date]

        payload = {
            "seDate": se_date,
            "channelCode": ["fixed_disc"],
            "pageSize": limit,
            "pageNum": 1
        }
        if stock_codes: payload["stock"] = stock_codes
        if keyword: payload["searchKey"] = [keyword]

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                results = []
                for item in data.get("data", []):
                    pub_time = item.get("publishTime", "")
                    
                    if start_date and end_date and len(start_date) > 10 and pub_time:
                        try:
                            pub_dt = datetime.strptime(pub_time, "%Y-%m-%d %H:%M:%S")
                            s_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                            e_dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
                            if not (s_dt <= pub_dt <= e_dt):
                                continue
                        except ValueError:
                            pass
                    
                    stock_code = ",".join(item.get("secCode", []))
                    stock_name = ",".join(item.get("secName", []))
                    title = item.get("title", "")
                    ann_id = item.get("id", "")
                    link = f"https://www.szse.cn/disclosure/listed/bulletinDetail/index.html?id={ann_id}"
                    results.append(f"[{stock_code}] {stock_name} - {title} ({pub_time}) | Link: {link}")
                return results
        except Exception as e:
            return [f"Error: {str(e)}"]
        return []

    def _query_sse(self, stock_codes, keyword, start_date, end_date, limit):
        url = "http://query.sse.com.cn/infodisplay/queryLatestBulletinNew.do"
        headers = {
            "Referer": "http://www.sse.com.cn/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        product_id = ",".join(stock_codes) if stock_codes else ""
        begin_d = start_date[:10] if len(start_date) > 10 else start_date
        end_d = end_date[:10] if len(end_date) > 10 else end_date
        
        params = {
            "isPagination": "true",
            "pageHelp.pageSize": limit,
            "pageHelp.pageNo": 1,
            "pageHelp.beginPage": 1,
            "pageHelp.cacheSize": 1,
            "pageHelp.endPage": 5,
            "productId": product_id,
            "keyWord": keyword if keyword else "",
            "reportType": "ALL",
            "securityType": "0101,120100,020100,020200,120200",
            "beginDate": begin_d,
            "endDate": end_d
        }
        
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                results = []
                for item in data.get("pageHelp", {}).get("data", []):
                    sec_code = item.get("security_Code", "")
                    title = item.get("title", "")
                    pub_time = item.get("SSEDate", "")
                    url_path = item.get("URL", "")
                    link = f"http://www.sse.com.cn{url_path}"
                    results.append(f"[{sec_code}] {title} ({pub_time}) | Link: {link}")
                return results
        except Exception as e:
            return [f"Error: {str(e)}"]
        return []

# Example usage for testing:
if __name__ == "__main__":
    plugin = StockAnnouncementPlugin()
    res = plugin.query_announcements(limit=20)
    import json
    print(json.dumps(res, indent=2, ensure_ascii=False))

from typing import List
import requests
import json

# 请求头信息
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Content-Type": "application/json",
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    "Referer": "https://www.eqxiu.com/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

eqxiustore_host_url = "https://msearch-api.eqxiu.com"
eqxiustore_search_url = "https://msearch-api.eqxiu.com/m/search/searchProducts"
basepreview_url = "https://www.eqxiu.com/mall/detail-{className}/"


class EqxiuStoreWebSearch:
    name: str = "eqxiu_template_search"
    description: str = """进行易企秀模板搜索，返回模板内容"""
    def getClassName(self, attrGroupId: int) -> str:      
        return 'h5' if attrGroupId == 2 else 'h5l' if attrGroupId == 10 else 'h5e' if attrGroupId == 11 else 'h2' if attrGroupId == 7 else 'gc' if attrGroupId == 14 else 'video' if attrGroupId == 15 else 'ebook' if attrGroupId == 18 else ''

    def execute(
        self,
        query: str,
        page_no: int = 1,
        num_results: int = 10,
        sort_by: str = "common_total|desc",
        color: str | None = None,
        price_range: str | None = None,
    ) -> List[str]:
        session = requests.Session()
        session.headers = HEADERS
        jsonquery = {
            "keywords": f"{query}",
            "sortBy": sort_by,
            "pageNo": page_no,
            "pageSize": num_results,
        }
        if color:
            jsonquery["color"] = color
        if price_range:
            jsonquery["priceRange"] = price_range
        res = session.post(url=eqxiustore_search_url, json=jsonquery)
        res.encoding = "utf-8"
        result = json.loads(res.text)
        if result["obj"]["total"] == 0:
            return []
        result_list = []
        for k in result["obj"]["dataList"]:
            className = self.getClassName(k["attrGroupId"])
            preview_url = basepreview_url.format(className=className)
            result_list.append({"title": k["title"], "link":preview_url+ str(k["id"]), "description": k["description"], "pv":k["views"]})
        return result_list

if __name__ == "__main__":
    import argparse
    import json
    
    from typing import List

    parser = argparse.ArgumentParser(description="Eqxiu Store Search")
    parser.add_argument( "--keywords", type=str, required=True, help="关键词")
    parser.add_argument("--pageNo", type=int, required=False, default=1, help="分页页码")
    parser.add_argument("--pageSize", type=int, required=False, default=10, help="每页条数")
    parser.add_argument("--sortBy", type=str, required=False, default="common_total|desc", help="排序字段，如 common_total|desc")
    parser.add_argument("--priceRange", type=str, required=False, default=None, help="价格范围，如 0a0 代表免费")
    parser.add_argument("--color", type=str, required=False, default=None, help="颜色，如 紫色、蓝色、粉色、红色、绿色、青色、橙色、黄色、黑色、白色、灰色")
    args = parser.parse_args()
    search = EqxiuStoreWebSearch()
    print(
        json.dumps(
            search.execute(
                args.keywords,
                args.pageNo,
                args.pageSize,
                sort_by=args.sortBy,
                color=args.color,
                price_range=args.priceRange,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
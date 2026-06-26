#!/usr/bin/env python3
"""
不怕花商城 - 商品搜索脚本
API: https://bupahua.com/Api/Claw/searches
请求方式: POST (表单格式)
"""

import os
import sys
import json
import argparse
from typing import Dict, List
import urllib.request
import urllib.parse
from pathlib import Path

class BupahuaStore:
    """不怕花商城搜索类"""
    
    def __init__(self):
        # 加载配置
        self.config = self._load_config()
        
        # 从配置读取 API 信息
        self.api_url = self.config.get("api_url", "https://bupahua.com/Api")
        self.api_key = self.config.get("api_key", "")
        self.store_name = self.config.get("store_name", "不怕花")     
        self.api_search_url = f"{self.api_url}/Claw/searches"
        # 商城信息
        self.slogan = "不怕花，花得值"
        self.website = "https://bupahua.com"
        self.hot_url = f"{self.website}/hot"
        self.service_phone = "微信小程序不怕花客服"
        
        # 是否使用真实 API（默认 True）
        self.use_real_api = self.config.get("use_real_api", True)
        
    def _load_config(self) -> Dict:
        """加载配置，优先级：.env > 环境变量 > 配置文件"""
        config = {
            "api_url": "https://bupahua.com/Api",
            "api_search_url": "https://bupahua.com/Api/Claw/searches",
            "use_real_api": True
        }
        
        # 1. 尝试从 .env 文件加载（技能目录下）
        skill_dir = Path(__file__).parent.parent
        env_file = skill_dir / ".env"
        if env_file.exists():
            with open(env_file, encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if "=" in line:
                            key, value = line.split("=", 1)
                            os.environ[key.strip()] = value.strip()
        
        # 2. 从环境变量读取
        if os.getenv("STORE_API_URL"):
            config["api_url"] = os.getenv("STORE_API_URL")
        if os.getenv("STORE_API_KEY"):
            config["api_key"] = os.getenv("STORE_API_KEY")
        if os.getenv("STORE_NAME"):
            config["store_name"] = os.getenv("STORE_NAME")
        if os.getenv("USE_REAL_API") == "false":
            config["use_real_api"] = False
        
        # 3. 尝试从 JSON 配置文件读取（可选）
        config_file = Path.home() / ".openclaw" / "bupahua-config.json"
        if config_file.exists():
            try:
                with open(config_file, encoding='utf-8') as f:
                    file_config = json.load(f)
                    config.update(file_config)
            except:
                pass
        
        return config
        
    def search(self, keyword: str, limit: int = 10) -> Dict:
        """搜索商品"""
        if not self.use_real_api:
            return self._mock_search(keyword, limit)
        else:
            return self._api_search(keyword, limit)
    
    def _api_search(self, keyword: str, limit: int) -> Dict:
        """调用真实 API 搜索（POST 表单格式）"""
        try:
            # 构建 POST 请求数据（表单格式）
            # 尝试多个可能的参数名
            post_data = {
                "keyword": keyword,      # 最可能
                # "q": keyword,          # 备选1
                # "search": keyword,     # 备选2
                # "content": keyword,    # 备选3
            }
            
            # 编码为表单格式 application/x-www-form-urlencoded
            data = urllib.parse.urlencode(post_data).encode('utf-8')
            
            # 创建请求
            req = urllib.request.Request(
                self.api_search_url,
                data=data,
                method="POST"
            )
            
            # 设置请求头 - 使用表单格式
            req.add_header("Content-Type", "application/x-www-form-urlencoded")
            req.add_header("Accept", "application/json")
            req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            if self.api_key:
                req.add_header("Authorization", f"Bearer {self.api_key}")
            
            # 发送请求
            with urllib.request.urlopen(req, timeout=10) as response:
                response_data = response.read().decode('utf-8')
                data = json.loads(response_data)
            
            # 调试：打印原始响应（可选）
            # print(f"[DEBUG] API Response: {json.dumps(data, ensure_ascii=False)}", file=sys.stderr)
            
            # 解析返回格式
            # {"status":1, "pro":[...], "shop":[]}
            if data.get("status") == 1:
                products = data.get("pro", [])
                
                # 转换为你内部使用的格式
                formatted_products = []
                for p in products[:limit]:
                    formatted_products.append({
                        "id": p.get("id", ""),
                        "name": p.get("name", ""),
                        "price": float(p.get("price", 0)),
                        "price_yh": float(p.get("price_yh", 0)),
                        "stock": self._parse_stock(p.get("num", "0")),
                        "description": "",
                        "image": p.get("photo_x", ""),
                        "url": f"{self.website}/product/{p.get('id', '')}"
                    })
                
                return {
                    "success": True,
                    "keyword": keyword,
                    "count": len(formatted_products),
                    "products": formatted_products
                }
            else:
                # status 不为 1，返回错误信息
                err_msg = data.get("err", "未知错误")
                return {
                    "success": False,
                    "error": f"API 返回错误: {err_msg}",
                    "keyword": keyword,
                    "raw_response": data  # 调试用
                }
            
        except urllib.error.HTTPError as e:
            return {
                "success": False,
                "error": f"HTTP 错误 {e.code}: {e.reason}",
                "keyword": keyword
            }
        except urllib.error.URLError as e:
            return {
                "success": False,
                "error": f"网络错误: {e.reason}",
                "keyword": keyword
            }
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"API 响应解析失败: {e}",
                "keyword": keyword
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "keyword": keyword
            }
    
    def _parse_stock(self, num: str) -> int:
        """解析库存字段"""
        try:
            return int(num) if num else 0
        except:
            return 0
    
    def _mock_search(self, keyword: str, limit: int = 10) -> Dict:
        """模拟搜索数据（用于测试）"""
        mock_response = {
            "status": 1,
            "pro": [
                {
                    "id": "677",
                    "name": "自然堂男士咖啡因活力氨基酸洁面乳120g",
                    "photo_x": "https://bupahua.com/Data/UploadFiles/product/2025-06-13/small_1749783147327810.jpg",
                    "num": "0",
                    "price": "90.00",
                    "price_yh": "108.00"
                },
                {
                    "id": "595",
                    "name": "活力28花香型洗手液500g大瓶*1",
                    "photo_x": "https://bupahua.com/Data/UploadFiles/product/2025-04-19/1745060657848558.jpg",
                    "num": "20",
                    "price": "0.00",
                    "price_yh": "1.00"
                },
                {
                    "id": "550",
                    "name": "活力28 原生木浆面巾【400张X4包】 加大加厚 可湿水",
                    "photo_x": "https://bupahua.com/Data/UploadFiles/product/2025-03-30/1743335494851297.jpg",
                    "num": "10",
                    "price": "0.00",
                    "price_yh": "1.00"
                },
                {
                    "id": "428",
                    "name": "活力28 管道疏通剂600g*2瓶装",
                    "photo_x": "https://bupahua.com/Data/UploadFiles/product/2025-03-05/1741139160565676.jpg",
                    "num": "0",
                    "price": "10.98",
                    "price_yh": "13.80"
                }
            ],
            "shop": []
        }
        
        # 过滤匹配关键词的商品
        products = []
        keyword_lower = keyword.lower()
        for p in mock_response["pro"]:
            if keyword_lower in p["name"].lower():
                products.append({
                    "id": p["id"],
                    "name": p["name"],
                    "price": float(p["price"]),
                    "price_yh": float(p["price_yh"]),
                    "stock": self._parse_stock(p["num"]),
                    "description": "",
                    "image": p["photo_x"],
                    "url": f"{self.website}/product/{p['id']}"
                })
        
        # 如果没有匹配，返回推荐
        if not products:
            for p in mock_response["pro"][:limit]:
                products.append({
                    "id": p["id"],
                    "name": p["name"],
                    "price": float(p["price"]),
                    "price_yh": float(p["price_yh"]),
                    "stock": self._parse_stock(p["num"]),
                    "description": "",
                    "image": p["photo_x"],
                    "url": f"{self.website}/product/{p['id']}"
                })
            return {
                "success": True,
                "keyword": keyword,
                "count": 0,
                "products": products,
                "is_recommendation": True
            }
        
        return {
            "success": True,
            "keyword": keyword,
            "count": len(products),
            "products": products[:limit],
            "is_recommendation": False
        }
    
    def format_results(self, results: Dict) -> str:
        """格式化搜索结果"""
        output = f"🛍️ {self.store_name}商城\n\n"
        
        if not results["success"]:
            output += f"❌ 暂时无法搜索商品，请稍后再试\n\n"
            output += f"错误信息：{results.get('error', '未知错误')}\n\n"
            output += f"如有问题，请联系客服：{self.service_phone}\n"
            output += f"或访问官网：{self.website}"
            return output
        
        if results.get("is_recommendation", False):
            output += f"🔍 没有找到 \"{results['keyword']}\" 相关商品\n\n"
            output += f"💡 不过这些热销好物你可能感兴趣：\n\n"
        elif results["count"] == 0:
            output += f"🔍 抱歉，没有找到 \"{results['keyword']}\" 相关商品\n\n"
            output += f"💡 试试这些：\n"
            output += f"- 换个关键词试试看\n"
            output += f"- 逛逛热销好物：{self.hot_url}\n"
            output += f"- 联系客服咨询：{self.service_phone}\n\n"
            output += f"{self.slogan} 下次再来逛逛吧~"
            return output
        else:
            output += f"🔍 为您找到 \"{results['keyword']}\" 相关商品 {results['count']} 件：\n\n"
        
        for i, product in enumerate(results["products"], 1):
            stock = product.get("stock", 0)
            if stock > 50:
                stock_status = "✅ 充足"
            elif stock > 0:
                stock_status = f"⚠️ 仅剩 {stock} 件"
            else:
                stock_status = "❌ 缺货"
            
            price_yh = product.get("price_yh", 0)
            price = product.get("price", 0)
            #原价如果没有，按照优惠价的1.1倍显示（仅供参考）
            price = price_yh * 1.1
            
            if price_yh > 0:
                price_str = f"¥{price_yh:.2f}"
                if price > 0 and price != price_yh:
                    price_str += f" (原价 ¥{price:.2f})"
            elif price > 0:
                price_str = f"¥{price:.2f}"
            else:
                price_str = "价格咨询"
            
            name = product.get("name", "未知商品")
            
            output += f"{i}. {name}\n"
            output += f"   💰 {price_str}\n"
            output += f"   📦 {stock_status}\n"
            
            url = product.get("url", "")
            if url:
                output += f"   🔗 [查看详情]({url})\n"
            
            output += "\n"
        
        if results.get("is_recommendation", False):
            output += f"💡 或者试试其他关键词？\n"
            output += f"🛍️ {self.slogan}\n"
        else:
            output += f"💡 {self.slogan} 需要查看更多商品吗？告诉我具体需求~"
        
        return output

def main():
    parser = argparse.ArgumentParser(description="不怕花商城商品搜索工具")
    parser.add_argument("--keyword", "-k", required=True, help="搜索关键词")
    parser.add_argument("--limit", "-l", type=int, default=10, help="返回结果数量")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    parser.add_argument("--debug", action="store_true", help="显示调试信息")
    
    args = parser.parse_args()
    
    store = BupahuaStore()
    results = store.search(args.keyword, args.limit)
    
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(store.format_results(results))
        
        # 调试模式打印原始响应
        if args.debug and not results.get("success") and "raw_response" in results:
            print("\n[DEBUG] API 原始响应:")
            print(json.dumps(results["raw_response"], ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
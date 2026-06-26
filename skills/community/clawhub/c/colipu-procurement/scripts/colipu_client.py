# -*- coding: utf-8 -*-
"""
科力普采购助手 API 客户端
封装登录、搜索、下单、查询等核心接口
"""

import os
import time
import requests
from typing import Optional, Dict, List
from dataclasses import dataclass, field


@dataclass
class ColipuConfig:
    """科力普配置（敏感信息从环境变量读取）"""
    base_url: str = "https://h5vip.colipu.com"
    site_id: int = 211
    warehouse_ids: List[int] = field(default_factory=lambda: [111])
    province_id: int = 2
    item_pic_path: str = "https://pic.colipu.com/pmspic/ItemPicture/"
    content_type: str = "application/json;charset=UTF-8"

    login_name: str = field(default_factory=lambda: os.getenv("COLIPU_LOGIN_NAME", ""))
    password: str = field(default_factory=lambda: os.getenv("COLIPU_PASSWORD", ""))
    customer_id: int = field(default_factory=lambda: int(os.getenv("COLIPU_CUSTOMER_ID", "0")))

    auto_relogin: bool = True


class ColipuAuthError(Exception):
    """登录失败 / 凭据缺失"""


class ColipuClient:
    """科力普 API 客户端"""

    _AUTH_FAIL_KEYWORDS = ("未登录", "请登录", "login", "Unauthorized", "session", "Session")

    def __init__(self, config: Optional[ColipuConfig] = None):
        self.config = config or ColipuConfig()
        self.session = requests.Session()
        self.egg_sess: Optional[str] = None
        self.account_info: Optional[Dict] = None
        self._login_in_progress = False

    def _get_headers(self, with_cookie: bool = True) -> Dict[str, str]:
        headers = {"content-type": self.config.content_type}
        if with_cookie and self.egg_sess:
            headers["Cookie"] = f"EGG_SESS={self.egg_sess}"
        return headers

    def _extract_egg_sess(self, response: requests.Response) -> Optional[str]:
        set_cookie = response.headers.get("Set-Cookie", "")
        for part in set_cookie.split(";"):
            part = part.strip()
            if part.startswith("EGG_SESS="):
                return part.split("=", 1)[1]
        if "EGG_SESS" in response.cookies:
            return response.cookies["EGG_SESS"]
        return None

    def _is_auth_failure(self, response: requests.Response) -> bool:
        """判断响应是否表示 EGG_SESS 失效（401 / 业务码登录态失败）"""
        if response.status_code == 401:
            return True
        try:
            data = response.json()
        except Exception:
            return False
        msg = str(data.get("message") or data.get("Message") or "")
        if any(kw in msg for kw in self._AUTH_FAIL_KEYWORDS):
            return True
        return False

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict] = None,
        json_body: Optional[Dict] = None,
        with_cookie: bool = True,
        _retried: bool = False,
    ) -> requests.Response:
        """统一请求入口，自动处理 EGG_SESS 失效重登一次"""
        url = f"{self.config.base_url}{path}"
        response = self.session.request(
            method,
            url,
            params=params,
            json=json_body,
            headers=self._get_headers(with_cookie=with_cookie),
        )
        response.raise_for_status()

        if (
            self.config.auto_relogin
            and with_cookie
            and not self._login_in_progress
            and not _retried
            and self._is_auth_failure(response)
            and self.config.login_name
            and self.config.password
        ):
            self.login()
            return self._request(
                method, path,
                params=params, json_body=json_body,
                with_cookie=with_cookie, _retried=True,
            )

        return response

    # ==================== 1. 登录 ====================

    def login(self, login_name: Optional[str] = None, password: Optional[str] = None) -> Dict:
        """账号密码登录，登录成功后写入 self.egg_sess / self.account_info。"""
        name = login_name or self.config.login_name
        pwd = password or self.config.password
        if not name or not pwd:
            raise ColipuAuthError(
                "缺少凭据：请设置环境变量 COLIPU_LOGIN_NAME / COLIPU_PASSWORD，"
                "或调用 login() 时显式传入"
            )

        self._login_in_progress = True
        try:
            payload = {
                "loginName": name,
                "pwd": pwd,
                "cleartext": "Y",
                "hasMobileLogin": False,
                "scene": "h5",
            }
            response = self.session.post(
                f"{self.config.base_url}/api/vip/login",
                json=payload,
                headers=self._get_headers(with_cookie=False),
            )
            response.raise_for_status()
            self.egg_sess = self._extract_egg_sess(response)
            data = response.json()
            if data.get("code") == 1:
                self.account_info = data.get("Data", {})
                if not self.config.customer_id:
                    self.config.customer_id = self.account_info.get("customerId", 0)
            return data
        finally:
            self._login_in_progress = False

    # ==================== 2. 商品搜索 ====================

    def search_products(
        self,
        keyword: str,
        warehouse_ids: Optional[List[int]] = None,
        province_id: Optional[int] = None,
        page_index: int = 1,
        page_size: int = 20,
        sort_type: int = 12,
        customer_id: Optional[int] = None,
        start_price: str = "",
        end_price: str = "",
    ) -> Dict:
        """关键词搜索商品。"""
        payload = {
            "siteId": self.config.site_id,
            "warehouseIds": warehouse_ids or self.config.warehouse_ids,
            "showContract": False,
            "sortType": sort_type,
            "keyWord": keyword,
            "pageIndex": page_index,
            "pageSize": page_size,
            "provinceId": province_id if province_id is not None else self.config.province_id,
            "startPrice": start_price,
            "endPrice": end_price,
            "consumer": {
                "customerId": customer_id or self.config.customer_id,
                "showType": "",
            },
        }
        return self._request("POST", "/api/b2bSearchApi/SearchByKeyWord", json_body=payload).json()

    def get_product_detail(self, item_id: int) -> Dict:
        """查询商品详情（属性、起订量等）。"""
        return self._request(
            "GET", "/api/b2bApi/GetAttributeGroupList",
            params={"ItemId": item_id},
        ).json()

    # ==================== 3. 收货地址 ====================

    def get_receivers(self) -> List[Dict]:
        """获取收货地址列表。"""
        return self._request("GET", "/api/accountApi/receiver/list/0").json()

    # ==================== 4. 成本中心 ====================

    def get_cost_centers(self, is_group_power: str = "N") -> Dict:
        """获取成本中心列表。"""
        return self._request(
            "GET", "/api/crm/getConcenter",
            params={"IsGroupPower": is_group_power},
        ).json()

    def get_valid_cost_centers(self) -> List[Dict]:
        """获取有效的成本中心（Status==A）。"""
        result = self.get_cost_centers()
        if result.get("IsSuccess"):
            return [c for c in result.get("Data", []) if c.get("Status") == "A"]
        return []

    # ==================== 5. 预提交订单（Direct=true） ====================

    def pre_create_order(
        self,
        receiver_id: int,
        cost_center_id: int,
        items: List[Dict],
        site_id: Optional[int] = None,
        item_pic_path: Optional[str] = None,
    ) -> Dict:
        """
        预提交订单（统一 Direct=true 模式，单 SKU / 多 SKU 都走这里，多 SKU 合并为一单）。

        Returns: Code==200 && Data.Success==true 时 Data.Message 为 GuId
        """
        payload = {
            "SiteId": site_id or self.config.site_id,
            "Direct": True,
            "Receiver": {
                "CostCenterId": cost_center_id,
                "ReceiverId": receiver_id,
            },
            "Items": items,
            "ItemPicPath": item_pic_path or self.config.item_pic_path,
        }
        return self._request("POST", "/api/confirm/create", json_body=payload).json()

    def build_order_item(
        self,
        item_sku_id: int,
        sale_price: float,
        sale_qty: int = 1,
        item_type: int = 1
    ) -> Dict:
        """
        构建订单商品项（Direct=true 模式，仅需 4 个核心字段）

        Args:
            item_sku_id: 商品 SKU ID（使用搜索结果的 ItemId）
            sale_price: 销售单价
            sale_qty: 购买数量
            item_type: 商品类型，普通商品固定 1

        Returns:
            商品项字典
        """
        return {
            "ItemSkuId": item_sku_id,
            "SalePrice": sale_price,
            "SaleQty": sale_qty,
            "ItemType": item_type
        }

    # ==================== 6. 确认提交订单 ====================

    def confirm_order(self, guid: str, so_evidence_list: Optional[List] = None) -> Dict:
        """
        确认提交订单。

        ⚠️ 订单创建是**异步**的：本接口返回 Data.Success==true 仅代表"提交成功"，
        SoId 通常**不会**直接返回，需通过 `get_order_create_result(guid)` 或
        `wait_order_create_result(guid)` 获取。
        """
        payload = {"GuId": guid, "SOEvidenceList": so_evidence_list or []}
        return self._request("POST", "/api/confirm/orderConfirm", json_body=payload).json()

    def get_order_create_result(self, guid: str) -> Dict:
        """
        单次查询订单异步创建结果。

        Args:
            guid: 预提交返回的 GuId（同 confirm_order 使用的 GuId）

        Returns:
            响应 JSON。成功时 `{"Code":200,"Data":<int 订单号>,"Message":null}`；
            订单仍在生成中时 Data 可能为 0 / null / 字符串。
        """
        payload = {"GuId": guid}
        return self._request("POST", "/api/confirm/getOrderCreateResult", json_body=payload).json()

    def wait_order_create_result(
        self,
        guid: str,
        timeout: float = 30.0,
        interval: float = 1.0,
    ) -> Optional[int]:
        """
        轮询 `getOrderCreateResult` 直到拿到订单号或超时。

        Args:
            guid: 预提交 GuId
            timeout: 总超时秒数
            interval: 轮询间隔秒数

        Returns:
            成功返回订单号（int），超时或失败返回 None
        """
        deadline = time.time() + timeout
        while True:
            result = self.get_order_create_result(guid)
            if result.get("Code") == 200:
                data = result.get("Data")
                try:
                    so_id = int(data) if data not in (None, "", 0, "0") else 0
                except (TypeError, ValueError):
                    so_id = 0
                if so_id > 0:
                    return so_id
            if time.time() >= deadline:
                return None
            time.sleep(interval)

    # ==================== 7. 查询订单 ====================

    def get_orders(
        self,
        order_type: int = 1,
        page_no: int = 1,
        page_size: int = 10,
        search_word: str = "",
        so_id: str = "",
        do_id: str = "",
    ) -> Dict:
        """查询订单列表。order_type: 1=全部 / 2=审批中 / 3=待发货 / 4=已发货。"""
        payload = {
            "type": order_type,
            "pageNo": page_no,
            "pageSize": page_size,
            "searchWord": search_word,
            "soId": so_id,
            "doId": do_id,
        }
        return self._request("POST", "/api/order/orderlist", json_body=payload).json()

    def get_order_detail(self, so_sys_no) -> Dict:
        """
        根据订单号查询订单详情。

        Args:
            so_sys_no: 订单系统号（即 wait_order_create_result 返回的 int，
                       或订单列表中的 soId / SysNo）

        Returns:
            响应 JSON：Code==1 表示成功，Data 含：
              - SoMaster: 订单主信息（SOID / Status / RealSOAmt / Receive* / ...）
              - SoItem:   订单商品明细数组（ProductName / Quantity / Price / RealPrice / ...）
              - DoList / AuditRecordList / SoEvidences: 配送 / 审批 / 凭证（可能为 null）
        """
        return self._request(
            "GET", "/api/order/getOrderDetail",
            params={"soSysno": so_sys_no},
        ).json()

    # ==================== 取消订单 ====================

    def cancel_order(self, order_id: str, cancel_reason: str = "用户取消") -> Dict:
        """取消订单。Code==1 且 Data=={"1":"操作成功"} 表示成功。"""
        payload = {"OrderId": order_id, "CancelReason": cancel_reason}
        return self._request("POST", "/api/order/CancelOrder", json_body=payload).json()

    # ==================== 一键下单 ====================

    def quick_order(
        self,
        keyword: str,
        qty: int = 1,
        receiver_id: Optional[int] = None,
        cost_center_id: Optional[int] = None,
        province_id: Optional[int] = None,
    ) -> Dict:
        """
        一键下单（搜索第一个商品并下单，Direct=true 模式）。

        ⚠️ 本方法**不包含用户确认环节**，仅用于自动化测试 / 内部脚本。
        Agent 流程请使用：pre_create_order → 展示订单 → 用户输入 y → confirm_order。
        """
        search_result = self.search_products(keyword=keyword, province_id=province_id)
        if search_result.get("Code") != 1 or not search_result.get("Data"):
            return {"success": False, "error": "未找到商品", "search_result": search_result}

        product = search_result["Data"][0]
        item_sku_id = product.get("ItemId") or product.get("ProductSkuId")
        sale_price = product.get("SalePrice", 0)

        receivers = self.get_receivers()
        if not receivers:
            return {"success": False, "error": "未找到收货地址"}
        receiver = receivers[0] if receiver_id is None else next(
            (r for r in receivers if r.get("ReceiverId") == receiver_id), receivers[0]
        )

        cost_centers = self.get_valid_cost_centers()
        if not cost_centers:
            return {"success": False, "error": "未找到有效成本中心"}
        cost_center = cost_centers[0] if cost_center_id is None else next(
            (c for c in cost_centers if c.get("CostCenterId") == cost_center_id), cost_centers[0]
        )

        items = [self.build_order_item(
            item_sku_id=item_sku_id,
            sale_price=sale_price,
            sale_qty=qty,
        )]

        pre_result = self.pre_create_order(
            receiver_id=receiver["ReceiverId"],
            cost_center_id=cost_center["CostCenterId"],
            items=items,
        )

        if pre_result.get("Code") != 200 or not pre_result.get("Data", {}).get("Success"):
            return {"success": False, "error": "预提交失败", "pre_result": pre_result}

        guid = pre_result["Data"]["Message"]
        confirm_result = self.confirm_order(guid=guid)
        success = (
            confirm_result.get("Code") == 200
            and confirm_result.get("Data", {}).get("Success")
        )

        so_id = self.wait_order_create_result(guid) if success else None

        return {
            "success": success,
            "product": product,
            "receiver": receiver,
            "cost_center": cost_center,
            "guid": guid,
            "confirm_result": confirm_result,
            "so_id": so_id,
        }


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 配置（敏感信息从环境变量读取）
    # export COLIPU_LOGIN_NAME="your_login_name"
    # export COLIPU_PASSWORD="your_password"
    # 注：customerId 会在登录成功后自动回填，无需手动设置

    client = ColipuClient()

    # 登录
    print("=== 登录 ===")
    login_result = client.login()
    print(f"登录结果: code={login_result.get('code')}")
    print(f"EGG_SESS: {client.egg_sess[:20] if client.egg_sess else 'N/A'}...")

    if login_result.get("code") != 1:
        print("登录失败,请检查账号密码")
        exit(1)

    # 搜索商品
    print("\n=== 搜索商品 ===")
    search_result = client.search_products(keyword="a4复印纸", province_id=2)
    print(f"搜索结果: {search_result.get('TotalCount')} 条")
    if search_result.get("Data"):
        product = search_result["Data"][0]
        print(f"第一个商品: {product.get('ItemFullName')} - ¥{product.get('SalePrice')}")

    # 获取收货地址
    print("\n=== 收货地址 ===")
    receivers = client.get_receivers()
    for r in receivers:
        print(f"  - {r.get('ContactName')}: {r.get('Area')} {r.get('Address')}")

    # 获取成本中心
    print("\n=== 成本中心 ===")
    cost_centers = client.get_valid_cost_centers()
    for c in cost_centers:
        print(f"  - {c.get('CostCenterName')} (ID: {c.get('CostCenterId')})")

    # 查询订单
    print("\n=== 最近订单 ===")
    orders = client.get_orders(order_type=1, page_size=5)
    print(f"订单数据: {orders.get('message', 'N/A')}")
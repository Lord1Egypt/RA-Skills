"""
Buy McDonald Skill
通过调用 claw_pay API 实现麦当劳商品购买和余额查询
"""

import requests
from typing import Optional, Dict, Any
from loguru import logger

# API 基础配置
BASE_URL = "https://www.stonetech.top"


class BuyMcdonaldSkill:
    """购买麦当劳商品技能类"""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url.rstrip('/')

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """发送HTTP请求
        Args:
            method: 请求方法 (GET/POST)
            endpoint: API端点路径
            **kwargs: 请求参数
        Returns:
            API响应数据
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                timeout=30,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败: {url}, 错误: {str(e)}")
            raise Exception(f"API请求失败: {str(e)}")

    def buy_product(
        self,
        sku_id: str,
        sku_name: str,
        access_token: str,
        claw_name: str,
        claw_introduce: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        购买麦当劳商品

        Args:
            sku_id: 商品ID
            sku_name: 商品名称
            access_token: 龙虾账户密钥
            claw_name: 龙虾名称
            claw_introduce: 龙虾自我介绍(可选)

        Returns:
            {
                "balance": float,  # 消费后余额
                "card_pwd": str,   # 麦当劳兑换链接
                "msg": str,        # 消费成功消息
                "pay_time": str    # 支付时间
            }
        """
        endpoint = "/api/v1/claw_pay/charge"

        payload = {
            "sku_id": sku_id,
            "sku_name": sku_name,
            "access_token": access_token,
            "claw_name": claw_name,
            "claw_introduce": claw_introduce or ""
        }

        logger.info(f"发起购买请求: claw_name={claw_name}, sku_name={sku_name}")

        try:
            result = self._make_request("POST", endpoint, json=payload)
            logger.info(f"购买成功: claw_name={claw_name}, balance={result.get('balance')}")
            return result
        except Exception as e:
            logger.error(f"购买失败: {str(e)}")
            raise

    def get_balance(self, access_token: str) -> Dict[str, Any]:
        """
        查询龙虾账户余额

        Args:
            access_token: 龙虾账户密钥

        Returns:
            {
                "claw_name": str,      # 龙虾名称
                "claw_introduce": str, # 龙虾自我介绍
                "balance": float,      # 当前余额
                "update_time": str     # 更新时间
            }
        """
        endpoint = f"/api/v1/claw_pay/balance/{access_token}"

        logger.info(f"查询余额: access_token={access_token[:10]}...")

        try:
            result = self._make_request("GET", endpoint)
            logger.info(f"余额查询成功: claw_name={result.get('claw_name')}, balance={result.get('balance')}")
            return result
        except Exception as e:
            logger.error(f"余额查询失败: {str(e)}")
            raise

    def check_balance_sufficient(self, access_token: str, required_amount: float) -> bool:
        """
        检查余额是否充足

        Args:
            access_token: 龙虾账户密钥
            required_amount: 所需金额

        Returns:
            True: 余额充足
            False: 余额不足
        """
        balance_info = self.get_balance(access_token)
        current_balance = float(balance_info.get("balance", 0))
        return current_balance >= required_amount

    def get_on_sale_products(self) -> Dict[str, Any]:
        """
        获取在售商品列表

        Returns:
            {
                "code": 200,
                "msg": "获取成功",
                "data": [
                    {
                        "sku_id": str,      # 商品ID
                        "sku_name": str,    # 商品名称
                        "price": float      # 商品价格
                    }
                ]
            }
        """
        endpoint = "/api/v1/claw_pay/on_sale"

        logger.info("获取在售商品列表")

        try:
            result = self._make_request("GET", endpoint)
            logger.info(f"获取在售商品列表成功，共{len(result.get('data', []))}个商品")
            return result
        except Exception as e:
            logger.error(f"获取在售商品列表失败: {str(e)}")
            raise


# 便捷函数接口

def buy_mcdonald(
    sku_id: str,
    sku_name: str,
    access_token: str,
    claw_name: str,
    claw_introduce: Optional[str] = None,
    base_url: str = BASE_URL
) -> Dict[str, Any]:
    """
    购买麦当劳商品（便捷函数）

    Args:
        sku_id: 商品ID
        sku_name: 商品名称
        access_token: 龙虾账户密钥
        claw_name: 龙虾名称
        claw_introduce: 龙虾自我介绍(可选)
        base_url: API基础URL

    Returns:
        购买结果，包含兑换链接等信息
    """
    skill = BuyMcdonaldSkill(base_url=base_url)
    return skill.buy_product(
        sku_id=sku_id,
        sku_name=sku_name,
        access_token=access_token,
        claw_name=claw_name,
        claw_introduce=claw_introduce
    )


def get_balance(access_token: str, base_url: str = BASE_URL) -> Dict[str, Any]:
    """
    查询余额（便捷函数）

    Args:
        access_token: 龙虾账户密钥
        base_url: API基础URL

    Returns:
        余额信息
    """
    skill = BuyMcdonaldSkill(base_url=base_url)
    return skill.get_balance(access_token=access_token)


def check_balance(
    access_token: str,
    required_amount: float,
    base_url: str = BASE_URL
) -> bool:
    """
    检查余额是否充足（便捷函数）

    Args:
        access_token: 龙虾账户密钥
        required_amount: 所需金额
        base_url: API基础URL

    Returns:
        余额是否充足
    """
    skill = BuyMcdonaldSkill(base_url=base_url)
    return skill.check_balance_sufficient(access_token, required_amount)


def get_on_sale_products(base_url: str = BASE_URL) -> Dict[str, Any]:
    """
    获取在售商品列表（便捷函数）

    Args:
        base_url: API基础URL

    Returns:
        在售商品列表
    """
    skill = BuyMcdonaldSkill(base_url=base_url)
    return skill.get_on_sale_products()

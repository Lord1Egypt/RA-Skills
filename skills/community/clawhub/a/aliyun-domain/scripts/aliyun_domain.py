#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云域名 API 客户端
通过阿里云 OpenAPI 管理域名资产

参考文档：https://next.api.aliyun.com/api/Domain/2018-01-29

⚠️ 安全规则：
所有涉及订单和资金操作的 API 调用，必须经过用户明确二次确认后才能执行！
包括：域名注册、续费、赎回、转移、锁定/解锁、联系人修改、DNS 修改等

🔗 续费链接功能（v1.10.0）：
自动为自有域名生成续费链接，格式：
https://wanwang.aliyun.com/buy/commonbuy?saleIDs={saleID}&duration=12&domainCartTradeParams=dr_ai_domain_general_buy
其中 saleID 从域名详情的 ProductId 字段获取
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any

# 阿里云 SDK
try:
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.acs_exception.exceptions import ClientException, ServerException

    # 导入正确的请求类
    from aliyunsdkdomain.request.v20180129 import (
        QueryDomainListRequest,
        QueryDomainByDomainNameRequest,
        QueryDomainByInstanceIdRequest,
        QueryDomainGroupListRequest,
        QueryTaskListRequest,
        QueryTaskDetailListRequest,
        SaveDomainGroupRequest,
        UpdateDomainToDomainGroupRequest,
        DeleteDomainGroupRequest,
        SaveSingleTaskForCreatingOrderRenewRequest,
        SaveBatchTaskForCreatingOrderRenewRequest,
        SaveBatchTaskForModifyingDomainDnsRequest,
        SaveSingleTaskForTransferProhibitionLockRequest,
        SaveBatchTaskForTransferProhibitionLockRequest,
        SaveSingleTaskForUpdatingContactInfoRequest,
        QueryTransferOutInfoRequest,
        SaveSingleTaskForCreatingDnsHostRequest,
        SaveSingleTaskForModifyingDnsHostRequest,
        SaveSingleTaskForDeletingDnsHostRequest,
        QueryDnsHostRequest,
        CheckDomainRequest,
        QueryContactInfoRequest,
        SaveRegistrantProfileRequest,
        QueryRegistrantProfilesRequest,
        SetDefaultRegistrantProfileRequest,
        SaveSingleTaskForDomainNameProxyServiceRequest,
        QueryTaskDetailHistoryRequest,
        QueryDomainSpecialBizInfoByDomainRequest,
        SaveSingleTaskForQueryingTransferAuthorizationCodeRequest,
        SaveSingleTaskForApprovingTransferOutRequest,
        SaveSingleTaskForCancelingTransferOutRequest,
        QueryTransferInListRequest,
        QueryTransferInByInstanceIdRequest,
        SaveSingleTaskForAssociatingEnsRequest,
        SaveSingleTaskForDisassociatingEnsRequest,
        QueryLocalEnsAssociationRequest,
        SetupDomainAutoRenewRequest,
        ScrollDomainListRequest,
        SaveSingleTaskForCreatingOrderActivateRequest,
        QueryChangeLogListRequest,
        SaveSingleTaskForSaveArtExtensionRequest,
        SaveSingleTaskForGenerateDomainCertificateRequest,
        QueryDomainRealNameVerificationInfoRequest,
        SaveTaskForSubmittingDomainRealNameVerificationByIdentityCredentialRequest,
        SaveTaskForUpdatingRegistrantInfoByIdentityCredentialRequest,
        QueryRegistrantProfileRealNameVerificationInfoRequest,
        SaveRegistrantProfileRealNameVerificationRequest,
        VerifyContactFieldRequest,
        SaveBatchTaskForUpdatingContactInfoByRegistrantProfileIdRequest,
        QueryContactInfoRequest,
    )

    SDK_AVAILABLE = True
except ImportError as e:
    SDK_AVAILABLE = False
    print(f"⚠️  阿里云 SDK 未安装：{e}")
    print("请运行：pip3 install aliyun-python-sdk-core aliyun-python-sdk-domain")


class AliyunDomainClient:
    """阿里云域名 API 客户端"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化客户端

        Args:
            config_path: 配置文件路径，默认使用 ~/.agents/skills/aliyun/config/credentials.json
                        如果设置了环境变量 ALIYUN_ACCESS_KEY_ID 和 ALIYUN_ACCESS_KEY_SECRET，则优先使用环境变量
        """
        if not SDK_AVAILABLE:
            raise ImportError("阿里云 SDK 未安装")

        # 优先从环境变量加载配置
        self.config = self._load_config_from_env()

        # 如果环境变量未设置，则从配置文件加载
        if not self.config:
            if config_path is None:
                config_path = (
                    Path(__file__).parent.parent / "config" / "credentials.json"
                )
            self.config = self._load_config(config_path)

        # 初始化 AcsClient
        self.client = AcsClient(
            self.config["access_key_id"],
            self.config["access_key_secret"],
            self.config.get("region_id", "cn-hangzhou"),
        )

        print(f"✅ 阿里云域名客户端已初始化")
        print(f"   地域：{self.config.get('region_id', 'cn-hangzhou')}")
        print(f"   AK: {self.config['access_key_id'][:10]}...")

    def _load_config_from_env(self) -> Optional[Dict]:
        """从环境变量加载配置"""
        access_key_id = os.getenv("ALIYUN_ACCESS_KEY_ID")
        access_key_secret = os.getenv("ALIYUN_ACCESS_KEY_SECRET")
        region_id = os.getenv("ALIYUN_REGION_ID", "cn-hangzhou")

        if access_key_id and access_key_secret:
            return {
                "access_key_id": access_key_id,
                "access_key_secret": access_key_secret,
                "region_id": region_id,
            }
        return None

    def _load_config(self, config_path: Path) -> Dict:
        """加载配置文件"""
        if not config_path.exists():
            raise FileNotFoundError(
                f"配置文件不存在：{config_path}\n"
                f"建议使用环境变量方式：\n"
                f'  export ALIYUN_ACCESS_KEY_ID="your-access-key-id"\n'
                f'  export ALIYUN_ACCESS_KEY_SECRET="your-access-key-secret"'
            )

        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        # 验证必要字段
        if "access_key_id" not in config or "access_key_secret" not in config:
            raise ValueError("配置文件缺少 access_key_id 或 access_key_secret")

        return config

    def _do_request(self, request) -> Dict:
        """执行 API 请求"""
        try:
            response = self.client.do_action_with_exception(request)
            return json.loads(response)
        except ClientException as e:
            print(f"❌ 客户端错误：{e}")
            raise
        except ServerException as e:
            print(f"❌ 服务端错误：{e}")
            raise

    # ==================== 域名查询 ====================

    def list_domains(
        self,
        page_num: int = 1,
        page_size: int = 100,
        keyword: Optional[str] = None,
        tld: Optional[str] = None,
        group_id: Optional[str] = None,
    ) -> List[Dict]:
        """
        查询域名列表

        Args:
            page_num: 页码
            page_size: 每页数量（最大 100）
            keyword: 关键词筛选
            tld: 域名后缀筛选（如 com, cn）
            group_id: 域名分组 ID

        Returns:
            域名列表
        """
        request = QueryDomainListRequest.QueryDomainListRequest()
        request.set_PageNum(page_num)
        request.set_PageSize(page_size)

        if keyword:
            request.set_KeyWord(keyword)
        if tld:
            request.set_Tld(tld)
        if group_id:
            request.set_GroupId(group_id)

        response = self._do_request(request)

        domains = []
        if "Data" in response and "Domain" in response["Data"]:
            domains = response["Data"]["Domain"]

        # 为每个域名添加续费链接
        enriched_domains = [self._enrich_domain_with_renew_link(d) for d in domains]
        return enriched_domains

    def scroll_domains(
        self, page_size: int = 100, keyword: Optional[str] = None
    ) -> List[Dict]:
        """
        滚动查询域名列表（适合大数据量）

        Args:
            page_size: 每页数量
            keyword: 关键词筛选

        Returns:
            域名列表
        """
        request = ScrollDomainListRequest.ScrollDomainListRequest()
        request.set_PageSize(page_size)

        if keyword:
            request.set_KeyWord(keyword)

        response = self._do_request(request)

        domains = []
        if "Data" in response and "Domain" in response["Data"]:
            domains = response["Data"]["Domain"]

        # 为每个域名添加续费链接
        enriched_domains = [self._enrich_domain_with_renew_link(d) for d in domains]
        return enriched_domains

    def _generate_renew_link(
        self, domain_info: Dict, duration: int = 12
    ) -> Optional[str]:
        """
        生成域名续费链接

        Args:
            domain_info: 域名信息字典，需包含 InstanceId 字段
            duration: 续费时长（月），默认 12 个月

        Returns:
            续费链接（Markdown 格式），如果无法生成则返回 None

        🔗 链接格式:
        https://wanwang.aliyun.com/buy/commonbuy?saleIDs={InstanceId}&duration=12&domainCartTradeParams=dr_ai_domain_general_buy

        ⚠️ 注意：saleIDs 参数使用 InstanceId（域名实例 ID），不是 ProductId
        InstanceId 格式：S + 年份 + 数字序列（如：S202621106478992）
        """
        # 获取 InstanceId（这才是正确的 saleIDs 参数）
        instance_id = domain_info.get("InstanceId")

        if not instance_id:
            return None

        # 构造续费链接
        base_url = "https://wanwang.aliyun.com/buy/commonbuy"
        params = {
            "saleIDs": instance_id,  # 使用 InstanceId 作为 saleIDs
            "duration": str(duration),
            "domainCartTradeParams": "dr_ai_domain_general_buy",
        }

        # 构建 URL
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        renew_url = f"{base_url}?{query_string}"

        # 返回 Markdown 格式链接
        domain_name = domain_info.get("DomainName", "域名")
        return f"[🔗 续费]({renew_url})"

    def _enrich_domain_with_renew_link(
        self, domain_info: Dict, duration: int = 12
    ) -> Dict:
        """
        为域名信息添加续费链接

        Args:
            domain_info: 域名信息字典
            duration: 续费时长（月），默认 12 个月

        Returns:
            包含续费链接的域名信息字典
        """
        # 复制字典，避免修改原始数据
        enriched = domain_info.copy()

        # 生成续费链接
        renew_link = self._generate_renew_link(domain_info, duration)
        if renew_link:
            enriched["RenewLink"] = renew_link
            enriched["SaleID"] = domain_info.get(
                "InstanceId"
            )  # 使用 InstanceId 作为 SaleID

        return enriched

    def query_domain_detail(self, domain_name: str) -> Dict:
        """
        查询域名详情（自动添加续费链接）

        Args:
            domain_name: 域名名称

        Returns:
            域名详细信息（包含 RenewLink 续费链接）
        """
        request = QueryDomainByDomainNameRequest.QueryDomainByDomainNameRequest()
        request.set_DomainName(domain_name)

        response = self._do_request(request)

        # 为域名详情添加续费链接
        if response:
            return self._enrich_domain_with_renew_link(response)
        return response

    def query_domain_by_instance(self, instance_id: str) -> Dict:
        """
        根据实例 ID 查询域名

        Args:
            instance_id: 域名实例 ID

        Returns:
            域名信息
        """
        request = QueryDomainByInstanceIdRequest.QueryDomainByInstanceIdRequest()
        request.set_InstanceID(instance_id)

        response = self._do_request(request)
        return response

    def check_domain(self, domain_name: str) -> Dict:
        """
        查询域名是否可注册

        Args:
            domain_name: 域名名称

        Returns:
            域名可用性信息，包含：
            - available: bool, 是否可注册 ⚠️ 注意是小写
            - premium: bool, 是否溢价域名
            - price_info: list, 价格信息
        """
        request = CheckDomainRequest.CheckDomainRequest()
        request.set_DomainName(domain_name)

        response = self._do_request(request)

        # 修复：API 返回格式是根级别的 Avail 字段，不是 Data.Avail
        # Avail: 1=可注册, 0=已注册, 2=不支持
        avail = response.get("Avail", 0)

        return {
            "available": avail == 1,
            "domain_name": response.get("DomainName", domain_name),
            "premium": response.get("Premium", False),
            "avail_code": avail,
            "price_info": response.get("StaticPriceInfo", {}).get("PriceInfo", []),
            "raw_response": response,
        }

    def prepare_domain_registration(
        self,
        domain_name: str,
        years: int = 1,
        registrant_profile_id: Optional[int] = None,
    ) -> Dict:
        """
        准备域名注册信息（用于确认，不实际提交）

        Args:
            domain_name: 域名名称
            years: 注册年限
            registrant_profile_id: 注册者信息模板 ID

        Returns:
            注册信息摘要，包含费用明细
        """
        # 先检查域名可用性
        avail_result = self.check_domain(domain_name)

        if not avail_result.get("available", False):
            return {"success": False, "message": "域名不可注册", "domain": domain_name}

        # 获取价格信息
        price_info = avail_result.get("price_info", [])
        total_price = 0
        for info in price_info:
            if info.get("period") == years * 12:
                total_price = info.get("money", 0)
                break

        # 获取注册者信息
        registrant_info = None
        if registrant_profile_id:
            profiles = self.query_registrant_profiles()
            for p in profiles:
                if p.get("RegistrantProfileId") == registrant_profile_id:
                    registrant_info = {
                        "name": p.get("ZhRegistrantName", p.get("RegistrantName")),
                        "organization": p.get(
                            "ZhRegistrantOrganization", p.get("RegistrantOrganization")
                        ),
                        "email": p.get("Email"),
                        "real_name_status": p.get("RealNameStatus"),
                    }
                    break

        return {
            "success": True,
            "action": "register_domain",
            "domain": domain_name,
            "years": years,
            "total_price": total_price,
            "currency": "CNY",
            "registrant_profile_id": registrant_profile_id,
            "registrant_info": registrant_info,
            "confirmation_required": True,
            "confirmation_message": f"""
🛒 域名注册确认

域名：{domain_name}
年限：{years} 年
费用：¥{total_price:.2f}
注册者：{registrant_info["name"] if registrant_info else "N/A"}
实名状态：{"✅ " + registrant_info["real_name_status"] if registrant_info else "未指定"}

⚠️ 此操作将产生实际费用，确认要注册吗？
回复"确认"继续。""",
        }

    def register_domain(
        self,
        domain_name: str,
        years: int = 1,
        registrant_profile_id: Optional[int] = None,
        confirmed: bool = False,
    ) -> Dict:
        """
        注册域名（创建订单）

        ⚠️ 安全规则：调用前必须获得用户明确确认！
        建议先调用 prepare_domain_registration() 获取确认信息

        Args:
            domain_name: 域名名称
            years: 注册年限（1-10）
            registrant_profile_id: 注册者信息模板 ID（可选）
            confirmed: 是否已确认（必须为 True 才能执行）

        Returns:
            任务结果，包含任务编号

        Raises:
            ValueError: 如果未确认就尝试执行
        """
        # 安全检查：必须确认后才能执行
        if not confirmed:
            raise ValueError(
                "⚠️ 安全警告：资金操作需要用户确认！\n"
                "请先调用 prepare_domain_registration() 获取确认信息，\n"
                "获得用户明确回复后，再调用此方法并设置 confirmed=True"
            )

        request = SaveSingleTaskForCreatingOrderActivateRequest.SaveSingleTaskForCreatingOrderActivateRequest()
        request.set_DomainName(domain_name)
        request.set_SubscriptionDuration(years)  # 使用 SubscriptionDuration

        # 如果提供了注册者模板 ID，使用它
        if registrant_profile_id:
            request.set_RegistrantProfileId(registrant_profile_id)

        response = self._do_request(request)
        return response

    def query_contact_info(self, domain_name: str) -> Dict:
        """
        查询域名联系人信息

        Args:
            domain_name: 域名名称

        Returns:
            联系人信息
        """
        request = QueryContactInfoRequest.QueryContactInfoRequest()
        request.set_DomainName(domain_name)

        response = self._do_request(request)
        return response

    # ==================== 域名管理 ====================

    def prepare_domain_renewal(self, domain_name: str, years: int = 1) -> Dict:
        """
        准备域名续费信息（用于确认，不实际提交）

        Args:
            domain_name: 域名名称
            years: 续费年限

        Returns:
            续费信息摘要，包含费用明细
        """
        # 查询域名详情
        try:
            detail = self.query_domain_detail(domain_name)
        except Exception as e:
            return {
                "success": False,
                "message": f"查询域名详情失败：{e}",
                "domain": domain_name,
            }

        # 提取域名信息
        expiration_date = detail.get("ExpirationDate", "未知")
        domain_status = detail.get("DomainStatus", "未知")

        # 估算费用（.com 为例，实际价格需根据后缀确定）
        # 注意：续费 API 不直接返回价格，需要预先估算或调用其他接口
        estimated_price_per_year = 85.0  # .com 默认价格
        total_price = estimated_price_per_year * years

        # 根据后缀调整估算价格
        tld = domain_name.split(".")[-1].lower()
        price_map = {
            "com": 85.0,
            "net": 85.0,
            "org": 85.0,
            "cn": 38.0,
            "com.cn": 38.0,
            "xyz": 7.0,
            "top": 15.0,
            "vip": 100.0,
            "io": 350.0,
            "ai": 800.0,
            "asia": 100.0,
            "me": 120.0,
        }
        estimated_price_per_year = price_map.get(tld, 85.0)
        total_price = estimated_price_per_year * years

        return {
            "success": True,
            "action": "renew_domain",
            "domain": domain_name,
            "years": years,
            "current_expiration": expiration_date,
            "domain_status": domain_status,
            "estimated_price_per_year": estimated_price_per_year,
            "total_price": total_price,
            "currency": "CNY",
            "confirmation_required": True,
            "confirmation_message": f"""
💰 域名续费确认

域名：{domain_name}
当前过期时间：{expiration_date}
续费年限：{years} 年
估算费用：¥{total_price:.2f} (¥{estimated_price_per_year:.2f}/年)
域名状态：{domain_status}

⚠️ 此操作将产生实际费用，确认要续费吗？
回复"确认"继续。""",
        }

    def renew_domain(
        self, domain_name: str, years: int = 1, confirmed: bool = False
    ) -> Dict:
        """
        域名续费（单个）

        ⚠️ 安全规则：调用前必须获得用户明确确认！
        建议先调用 prepare_domain_renewal() 获取确认信息

        Args:
            domain_name: 域名名称
            years: 续费年限（1-10）
            confirmed: 是否已确认（必须为 True 才能执行）

        Returns:
            任务结果

        Raises:
            ValueError: 如果未确认就尝试执行
        """
        # 安全检查：必须确认后才能执行
        if not confirmed:
            raise ValueError(
                "⚠️ 安全警告：资金操作需要用户确认！\n"
                "请先调用 prepare_domain_renewal() 获取确认信息，\n"
                "获得用户明确回复后，再调用此方法并设置 confirmed=True"
            )

        request = SaveSingleTaskForCreatingOrderRenewRequest.SaveSingleTaskForCreatingOrderRenewRequest()
        request.set_DomainName(domain_name)
        request.set_SubscriptionDuration(years)  # 使用 SubscriptionDuration

        response = self._do_request(request)
        return response

    def batch_renew_domains(
        self, domain_names: List[str], years: int = 1, confirmed: bool = False
    ) -> Dict:
        """
        批量域名续费

        ⚠️ 安全规则：调用前必须获得用户明确确认！

        Args:
            domain_names: 域名名称列表
            years: 续费年限
            confirmed: 是否已确认（必须为 True 才能执行）

        Returns:
            任务结果

        Raises:
            ValueError: 如果未确认就尝试执行
        """
        if not confirmed:
            raise ValueError(
                "⚠️ 安全警告：资金操作需要用户确认！\n"
                "请获得用户明确回复后，再调用此方法并设置 confirmed=True"
            )

        request = SaveBatchTaskForCreatingOrderRenewRequest.SaveBatchTaskForCreatingOrderRenewRequest()

        # 设置域名列表
        domain_list = [
            {"DomainName": name, "SubscriptionYears": years} for name in domain_names
        ]
        request.set_DomainList(domain_list)

        response = self._do_request(request)
        return response

    def prepare_dns_modification(
        self, domain_name: str, dns_servers: List[str]
    ) -> Dict:
        """
        准备 DNS 修改信息（用于确认）

        Args:
            domain_name: 域名名称
            dns_servers: 新 DNS 服务器列表

        Returns:
            修改信息摘要
        """
        # 查询当前 DNS
        try:
            detail = self.query_domain_detail(domain_name)
            current_dns = detail.get("DnsList", {}).get("Dns", [])
        except Exception:
            current_dns = []

        return {
            "success": True,
            "action": "modify_dns",
            "domain": domain_name,
            "current_dns": current_dns,
            "new_dns": dns_servers,
            "confirmation_required": True,
            "confirmation_message": f"""
🌐 修改 DNS 服务器确认

域名：{domain_name}
当前 DNS: {", ".join(current_dns) if current_dns else "未知"}
新 DNS: {", ".join(dns_servers)}

⚠️ 此操作将影响域名解析，确认要修改吗？
回复"确认"继续。""",
        }

    def modify_domain_dns(
        self, domain_name: str, dns_servers: List[str], confirmed: bool = False
    ) -> Dict:
        """
        修改域名 DNS 服务器（单个）

        ⚠️ 安全规则：调用前必须获得用户明确确认！

        Args:
            domain_name: 域名名称
            dns_servers: DNS 服务器列表
            confirmed: 是否已确认（必须为 True 才能执行）

        Returns:
            任务结果

        Raises:
            ValueError: 如果未确认就尝试执行
        """
        if not confirmed:
            raise ValueError(
                "⚠️ 安全警告：敏感操作需要用户确认！\n"
                "请先调用 prepare_dns_modification() 获取确认信息，\n"
                "获得用户明确回复后，再调用此方法并设置 confirmed=True"
            )

        # 使用批量任务 API 进行单个域名 DNS 修改
        request = SaveBatchTaskForModifyingDomainDnsRequest.SaveBatchTaskForModifyingDomainDnsRequest()

        # 设置域名和 DNS 服务器
        request.set_DomainNames(domain_name)
        request.set_DomainNameServers(dns_servers)
        request.set_AliyunDns(False)  # 使用非阿里云 DNS

        response = self._do_request(request)
        return response

    def set_transfer_prohibition_lock(
        self, domain_name: str, lock_status: bool
    ) -> Dict:
        """
        设置域名转移锁（单个）

        Args:
            domain_name: 域名名称
            lock_status: True=开启转移锁，False=关闭转移锁

        Returns:
            任务结果
        """
        request = SaveSingleTaskForTransferProhibitionLockRequest.SaveSingleTaskForTransferProhibitionLockRequest()
        request.set_DomainName(domain_name)
        request.set_LockStatus(lock_status)

        response = self._do_request(request)
        return response

    def query_transfer_out_info(self, domain_name: str) -> Dict:
        """
        查询域名转出信息

        Args:
            domain_name: 域名名称

        Returns:
            转出信息
        """
        request = QueryTransferOutInfoRequest.QueryTransferOutInfoRequest()
        request.set_DomainName(domain_name)

        response = self._do_request(request)
        return response

    def query_transfer_authorization_code(self, domain_name: str) -> Dict:
        """
        查询域名转移密码

        Args:
            domain_name: 域名名称

        Returns:
            转移密码信息
        """
        request = SaveSingleTaskForQueryingTransferAuthorizationCodeRequest.SaveSingleTaskForQueryingTransferAuthorizationCodeRequest()
        request.set_DomainName(domain_name)

        response = self._do_request(request)
        return response

    def approve_transfer_out(self, domain_name: str) -> Dict:
        """
        批准域名转出

        Args:
            domain_name: 域名名称

        Returns:
            任务结果
        """
        request = SaveSingleTaskForApprovingTransferOutRequest.SaveSingleTaskForApprovingTransferOutRequest()
        request.set_DomainName(domain_name)

        response = self._do_request(request)
        return response

    def cancel_transfer_out(self, domain_name: str) -> Dict:
        """
        取消域名转出

        Args:
            domain_name: 域名名称

        Returns:
            任务结果
        """
        request = SaveSingleTaskForCancelingTransferOutRequest.SaveSingleTaskForCancelingTransferOutRequest()
        request.set_DomainName(domain_name)

        response = self._do_request(request)
        return response

    def setup_auto_renew(
        self, domain_name: str, auto_renew: bool, duration: int = 1
    ) -> Dict:
        """
        设置域名自动续费

        Args:
            domain_name: 域名名称
            auto_renew: 是否自动续费
            duration: 续费时长（年）

        Returns:
            任务结果
        """
        request = SetupDomainAutoRenewRequest.SetupDomainAutoRenewRequest()
        request.set_DomainName(domain_name)
        request.set_AutoRenew(auto_renew)
        request.set_Duration(duration)

        response = self._do_request(request)
        return response

    # ==================== 任务管理 ====================

    def query_task_list(
        self,
        page_num: int = 1,
        page_size: int = 100,
        status: Optional[str] = None,
        begin_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> List[Dict]:
        """
        查询任务列表

        Args:
            page_num: 页码
            page_size: 每页数量
            status: 任务状态（RUNNING, SUCCESS, FAIL）
            begin_time: 开始时间（ISO8601）
            end_time: 结束时间（ISO8601）

        Returns:
            任务列表
        """
        request = QueryTaskListRequest.QueryTaskListRequest()
        request.set_PageNum(page_num)
        request.set_PageSize(page_size)

        if status:
            request.set_TaskStatus(status)
        if begin_time:
            request.set_BeginCreateTime(begin_time)
        if end_time:
            request.set_EndCreateTime(end_time)

        response = self._do_request(request)

        tasks = []
        if "Data" in response and "Data" in response["Data"]:
            tasks = response["Data"]["Data"]

        return tasks

    def query_task_detail(
        self, task_no: str, page_num: int = 1, page_size: int = 100
    ) -> List[Dict]:
        """
        查询任务详情

        Args:
            task_no: 任务编号
            page_num: 页码
            page_size: 每页数量

        Returns:
            任务详情列表
        """
        request = QueryTaskDetailListRequest.QueryTaskDetailListRequest()
        request.set_TaskNo(task_no)
        request.set_PageNum(page_num)
        request.set_PageSize(page_size)

        response = self._do_request(request)

        details = []
        if "Data" in response and "Data" in response["Data"]:
            details = response["Data"]["Data"]

        return details

    def query_task_history(self, task_no: str) -> List[Dict]:
        """
        查询任务历史详情

        Args:
            task_no: 任务编号

        Returns:
            任务历史详情
        """
        request = QueryTaskDetailHistoryRequest.QueryTaskDetailHistoryRequest()
        request.set_TaskNo(task_no)

        response = self._do_request(request)

        details = []
        if "Data" in response and "Data" in response["Data"]:
            details = response["Data"]["Data"]

        return details

    # ==================== 域名组管理 ====================

    def create_domain_group(self, group_name: str) -> Dict:
        """
        创建域名分组

        Args:
            group_name: 分组名称

        Returns:
            分组信息
        """
        request = SaveDomainGroupRequest.SaveDomainGroupRequest()
        request.set_GroupName(group_name)

        response = self._do_request(request)
        return response

    def query_domain_group_list(self) -> List[Dict]:
        """
        查询域名分组列表

        Returns:
            分组列表
        """
        request = QueryDomainGroupListRequest.QueryDomainGroupListRequest()

        response = self._do_request(request)

        groups = []
        if "Data" in response and "DomainGroup" in response["Data"]:
            groups = response["Data"]["DomainGroup"]

        return groups

    def update_domain_to_group(self, domain_name: str, group_id: str) -> Dict:
        """
        将域名更新到指定分组

        Args:
            domain_name: 域名名称
            group_id: 分组 ID

        Returns:
            任务结果
        """
        request = UpdateDomainToDomainGroupRequest.UpdateDomainToDomainGroupRequest()
        request.set_DomainName(domain_name)
        request.set_GroupID(group_id)

        response = self._do_request(request)
        return response

    def delete_domain_group(self, group_id: str) -> Dict:
        """
        删除域名分组

        Args:
            group_id: 分组 ID

        Returns:
            删除结果
        """
        request = DeleteDomainGroupRequest.DeleteDomainGroupRequest()
        request.set_GroupID(group_id)

        response = self._do_request(request)
        return response

    # ==================== DNS 主机管理 ====================

    def create_dns_host(
        self, domain_name: str, host_name: str, ip_addresses: List[str]
    ) -> Dict:
        """
        创建 DNS 主机

        Args:
            domain_name: 域名名称
            host_name: 主机名称（如 ns1.example.com）
            ip_addresses: IP 地址列表

        Returns:
            任务结果
        """
        request = SaveSingleTaskForCreatingDnsHostRequest.SaveSingleTaskForCreatingDnsHostRequest()
        request.set_DomainName(domain_name)
        request.set_HostName(host_name)

        # 设置 IP 地址
        ip_list = [{"Ip": ip} for ip in ip_addresses]
        request.set_Ip(ip_list)

        response = self._do_request(request)
        return response

    def modify_dns_host(
        self, domain_name: str, host_name: str, new_ip_addresses: List[str]
    ) -> Dict:
        """
        修改 DNS 主机

        Args:
            domain_name: 域名名称
            host_name: 主机名称
            new_ip_addresses: 新 IP 地址列表

        Returns:
            任务结果
        """
        request = SaveSingleTaskForModifyingDnsHostRequest.SaveSingleTaskForModifyingDnsHostRequest()
        request.set_DomainName(domain_name)
        request.set_HostName(host_name)

        # 设置新 IP 地址
        ip_list = [{"Ip": ip} for ip in new_ip_addresses]
        request.set_Ip(ip_list)

        response = self._do_request(request)
        return response

    def delete_dns_host(self, domain_name: str, host_name: str) -> Dict:
        """
        删除 DNS 主机

        Args:
            domain_name: 域名名称
            host_name: 主机名称

        Returns:
            任务结果
        """
        request = SaveSingleTaskForDeletingDnsHostRequest.SaveSingleTaskForDeletingDnsHostRequest()
        request.set_DomainName(domain_name)
        request.set_HostName(host_name)

        response = self._do_request(request)
        return response

    def query_dns_host(self, domain_name: str) -> List[Dict]:
        """
        查询 DNS 主机

        Args:
            domain_name: 域名名称

        Returns:
            DNS 主机列表
        """
        request = QueryDnsHostRequest.QueryDnsHostRequest()
        request.set_DomainName(domain_name)

        response = self._do_request(request)

        hosts = []
        if "Data" in response and "DnsHost" in response["Data"]:
            hosts = response["Data"]["DnsHost"]

        return hosts

    # ==================== 注册者信息 ====================

    def create_registrant_profile(self, profile_data: Dict) -> Dict:
        """
        创建注册者信息模板

        Args:
            profile_data: 注册者信息
                - RegistrantOrganization: 组织名称
                - RegistrantName: 姓名
                - Province: 省
                - City: 市
                - Address: 地址
                - PostalCode: 邮编
                - Country: 国家
                - Email: 邮箱
                - TelArea: 电话区号
                - Telephone: 电话
                - TelExt: 分机号

        Returns:
            创建结果
        """
        request = SaveRegistrantProfileRequest.SaveRegistrantProfileRequest()

        for key, value in profile_data.items():
            setter = f"set_{key}"
            if hasattr(request, setter):
                getattr(request, setter)(value)

        response = self._do_request(request)
        return response

    def query_registrant_profiles(
        self, page_num: int = 1, page_size: int = 100
    ) -> List[Dict]:
        """
        查询注册者信息模板列表

        Args:
            page_num: 页码
            page_size: 每页数量

        Returns:
            注册者信息列表
        """
        request = QueryRegistrantProfilesRequest.QueryRegistrantProfilesRequest()
        request.set_PageNum(page_num)
        request.set_PageSize(page_size)

        response = self._do_request(request)

        profiles = []
        if "Data" in response and "RegistrantProfile" in response["Data"]:
            profiles = response["Data"]["RegistrantProfile"]

        return profiles

    def set_default_registrant_profile(self, profile_id: int) -> Dict:
        """
        设置默认注册者信息模板

        Args:
            profile_id: 模板 ID

        Returns:
            设置结果
        """
        request = (
            SetDefaultRegistrantProfileRequest.SetDefaultRegistrantProfileRequest()
        )
        request.set_RegistrantProfileID(profile_id)

        response = self._do_request(request)
        return response

    # ==================== 辅助方法 ====================

    def query_expiring_domains(self, days: int = 30) -> List[Dict]:
        """
        查询即将过期的域名

        Args:
            days: 天数范围

        Returns:
            即将过期的域名列表
        """
        expiring = []
        page = 1

        while True:
            domains = self.list_domains(page_num=page, page_size=100)
            if not domains:
                break

            cutoff_date = datetime.now() + timedelta(days=days)

            for domain in domains:
                if "ExpirationDate" in domain:
                    try:
                        exp_date = datetime.strptime(
                            domain["ExpirationDate"], "%Y-%m-%d %H:%M:%S"
                        )
                        if exp_date <= cutoff_date:
                            expiring.append(domain)
                    except Exception:
                        pass

            page += 1
            if len(domains) < 100:
                break

        return expiring

    def get_all_domains(self) -> List[Dict]:
        """
        获取所有域名（自动分页，包含续费链接）

        Returns:
            所有域名列表（每个域名包含 RenewLink 续费链接）
        """
        all_domains = []
        page = 1

        while True:
            domains = self.list_domains(page_num=page, page_size=100)
            if not domains:
                break

            # 为每个域名添加续费链接
            enriched_domains = [self._enrich_domain_with_renew_link(d) for d in domains]
            all_domains.extend(enriched_domains)

            if len(domains) < 100:
                break

            page += 1

        return all_domains

    def get_domain_statistics(self) -> Dict:
        """
        获取域名统计信息

        Returns:
            统计信息
        """
        domains = self.get_all_domains()

        # 按后缀统计
        tld_count = {}
        # 按状态统计
        status_count = {}
        # 即将过期数量
        expiring_30 = 0
        expiring_90 = 0

        now = datetime.now()

        for domain in domains:
            # 后缀统计
            name = domain.get("DomainName", "")
            if "." in name:
                tld = name.split(".")[-1]
                tld_count[tld] = tld_count.get(tld, 0) + 1

            # 状态统计
            status = domain.get("DomainStatus", "Unknown")
            status_count[status] = status_count.get(status, 0) + 1

            # 过期时间统计
            if "ExpirationDate" in domain:
                try:
                    exp_date = datetime.strptime(
                        domain["ExpirationDate"], "%Y-%m-%d %H:%M:%S"
                    )
                    days_left = (exp_date - now).days

                    if days_left <= 30:
                        expiring_30 += 1
                    if days_left <= 90:
                        expiring_90 += 1
                except Exception:
                    pass

        return {
            "total": len(domains),
            "tld_distribution": tld_count,
            "status_distribution": status_count,
            "expiring_30_days": expiring_30,
            "expiring_90_days": expiring_90,
        }


def main():
    """主函数 - 命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="阿里云域名管理工具")
    subparsers = parser.add_subparsers(dest="action", help="操作类型")

    # list 命令
    list_parser = subparsers.add_parser("list", help="查询域名列表")
    list_parser.add_argument("--keyword", "-k", help="关键词筛选")
    list_parser.add_argument("--tld", "-t", help="域名后缀筛选")
    list_parser.add_argument("--page", type=int, default=1, help="页码")
    list_parser.add_argument("--page-size", type=int, default=100, help="每页数量")

    # detail 命令
    detail_parser = subparsers.add_parser("detail", help="查询域名详情")
    detail_parser.add_argument("--domain", "-d", required=True, help="域名名称")

    # expiring 命令
    expiring_parser = subparsers.add_parser("expiring", help="查询即将过期域名")
    expiring_parser.add_argument("--days", type=int, default=30, help="过期天数范围")

    # renew 命令
    renew_parser = subparsers.add_parser("renew", help="域名续费")
    renew_parser.add_argument("--domain", "-d", required=True, help="域名名称")
    renew_parser.add_argument("--years", type=int, default=1, help="续费年限")

    # tasks 命令
    tasks_parser = subparsers.add_parser("tasks", help="查询任务列表")
    tasks_parser.add_argument("--status", help="任务状态筛选")
    tasks_parser.add_argument("--task-no", help="任务编号")

    # groups 命令
    groups_parser = subparsers.add_parser("groups", help="域名分组管理")
    groups_parser.add_argument("--create", help="创建分组")
    groups_parser.add_argument("--list", action="store_true", help="列出分组")

    # dns 命令
    dns_parser = subparsers.add_parser("dns", help="DNS 主机管理")
    dns_parser.add_argument("--domain", "-d", required=True, help="域名名称")
    dns_parser.add_argument("--list", action="store_true", help="列出 DNS 主机")

    # stats 命令
    stats_parser = subparsers.add_parser("stats", help="域名统计")

    # contact 命令
    contact_parser = subparsers.add_parser("contact", help="查询联系人信息")
    contact_parser.add_argument("--domain", "-d", required=True, help="域名名称")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        return

    try:
        client = AliyunDomainClient()

        if args.action == "list":
            print("🦐 阿里云域名列表")
            print("=" * 100)
            print(f"{'域名':<45} {'过期时间':<20} {'状态':<15} {'自动续费':<10}")
            print("-" * 100)

            domains = client.list_domains(
                page_num=args.page,
                page_size=args.page_size,
                keyword=args.keyword,
                tld=args.tld,
            )

            for domain in domains:
                name = domain.get("DomainName", "N/A")[:43]
                exp_date = (
                    domain.get("ExpirationDate", "N/A")[:19]
                    if domain.get("ExpirationDate")
                    else "N/A"
                )
                status = domain.get("DomainStatus", "N/A")
                auto_renew = "是" if domain.get("AutoRenew", False) else "否"
                print(f"{name:<45} {exp_date:<20} {status:<15} {auto_renew:<10}")

            print("-" * 100)
            print(f"共 {len(domains)} 个域名 (第 {args.page} 页)")

        elif args.action == "detail":
            detail = client.query_domain_detail(args.domain)
            print(f"🦐 域名详情：{args.domain}")
            print("=" * 80)

            # 格式化输出关键信息
            if "Data" in detail:
                data = detail["Data"]
                for key in [
                    "DomainName",
                    "RegistrationDate",
                    "ExpirationDate",
                    "DomainStatus",
                    "AutoRenew",
                    "DnsName",
                ]:
                    if key in data:
                        print(f"{key}: {data[key]}")
            else:
                print(json.dumps(detail, ensure_ascii=False, indent=2))

        elif args.action == "expiring":
            print(f"🦐 即将过期域名（{args.days}天内）")
            print("=" * 80)

            expiring = client.query_expiring_domains(days=args.days)
            for domain in expiring:
                name = domain.get("DomainName", "N/A")
                exp_date = domain.get("ExpirationDate", "N/A")
                print(f"{name} - {exp_date}")

            print("-" * 80)
            print(f"共 {len(expiring)} 个域名即将过期")

        elif args.action == "renew":
            result = client.renew_domain(args.domain, years=args.years)
            print(f"🦐 域名续费任务已提交")
            print(f"任务编号：{result.get('TaskNo', 'N/A')}")

        elif args.action == "tasks":
            if args.task_no:
                details = client.query_task_detail(args.task_no)
                print(f"🦐 任务详情：{args.task_no}")
                for detail in details:
                    print(json.dumps(detail, ensure_ascii=False, indent=2))
            else:
                print("🦐 任务列表")
                print("=" * 80)
                tasks = client.query_task_list(status=args.status)
                for task in tasks[:20]:  # 只显示前 20 个
                    task_no = task.get("TaskNo", "N/A")
                    task_type = task.get("TaskType", "N/A")
                    status = task.get("TaskStatus", "N/A")
                    create_time = task.get("CreateTime", "N/A")
                    print(f"{task_no} - {task_type} - {status} - {create_time}")
                print("-" * 80)
                print(f"共 {len(tasks)} 个任务")

        elif args.action == "groups":
            if args.create:
                result = client.create_domain_group(args.create)
                print(f"🦐 域名分组已创建")
                print(f"分组 ID: {result.get('DomainGroupId', 'N/A')}")
            else:
                print("🦐 域名分组列表")
                print("=" * 80)
                groups = client.query_domain_group_list()
                for group in groups:
                    group_id = group.get("DomainGroupId", "N/A")
                    group_name = group.get("GroupName", "N/A")
                    print(f"{group_id} - {group_name}")
                print("-" * 80)
                print(f"共 {len(groups)} 个分组")

        elif args.action == "dns":
            hosts = client.query_dns_host(args.domain)
            print(f"🦐 域名 DNS 主机：{args.domain}")
            print("=" * 80)

            for host in hosts:
                host_name = host.get("HostName", "N/A")
                ips = host.get("Ips", {}).get("Ip", [])
                if isinstance(ips, str):
                    ips = [ips]
                print(f"{host_name} - {', '.join(ips)}")

            print("-" * 80)
            print(f"共 {len(hosts)} 个 DNS 主机")

        elif args.action == "stats":
            stats = client.get_domain_statistics()
            print("🦐 域名统计信息")
            print("=" * 80)
            print(f"总域名数：{stats['total']}")
            print(f"即将过期 (30 天): {stats['expiring_30_days']}")
            print(f"即将过期 (90 天): {stats['expiring_90_days']}")
            print()
            print("域名后缀分布:")
            for tld, count in sorted(
                stats["tld_distribution"].items(), key=lambda x: -x[1]
            )[:10]:
                print(f"  .{tld}: {count}")
            print()
            print("域名状态分布:")
            for status, count in sorted(
                stats["status_distribution"].items(), key=lambda x: -x[1]
            ):
                print(f"  {status}: {count}")

        elif args.action == "contact":
            contact = client.query_contact_info(args.domain)
            print(f"🦐 域名联系人信息：{args.domain}")
            print("=" * 80)

            if "Data" in contact:
                data = contact["Data"]
                for key in [
                    "RegistrantName",
                    "RegistrantOrganization",
                    "Email",
                    "Telephone",
                    "Province",
                    "City",
                    "Address",
                ]:
                    if key in data:
                        print(f"{key}: {data[key]}")
            else:
                print(json.dumps(contact, ensure_ascii=False, indent=2))

    except FileNotFoundError as e:
        print(f"❌ 配置错误：{e}")
        print("\n💡 请先配置阿里云凭证:")
        print(f"   cp config/credentials.json.example config/credentials.json")
        print(f"   然后编辑 config/credentials.json 填入您的 AK/SK")
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()

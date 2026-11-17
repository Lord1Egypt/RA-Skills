#!/usr/bin/env python3
"""
Fin-PIPL — 金融行业个人信息保护合规检查工具
基于《个人信息保护法》《个人金融信息保护规范》(JR/T 0171)、《金融数据安全分级指南》(JR/T 0197)

适用场景：银行 / 证券 / 保险 / 支付
运行模式：纯本地，无网络请求
"""

import argparse
import datetime
import json
import sys
import os
from dataclasses import dataclass, field, asdict
from typing import List, Optional


# ============================================================
# 数据模型
# ============================================================

@dataclass
class CheckResult:
    check_id: str
    description: str
    severity: str       # "PASS" / "WARN" / "FAIL"
    passed: bool
    details: str
    recommendation: str
    regulation_ref: str


@dataclass
class CheckReport:
    tool_name: str
    version: str
    timestamp: str
    scenario: str
    summary: dict
    items: list
    raw_items: list = field(default_factory=list)

    def to_dict(self):
        return {
            "tool": self.tool_name,
            "version": self.version,
            "timestamp": self.timestamp,
            "scenario": self.scenario,
            "summary": self.summary,
            "items": self.items,
        }


# ============================================================
# 金融行业检查项
# ============================================================

class FinPIPLChecker:
    """金融行业 PIPL 合规检查引擎"""

    SCENARIOS = {
        "banking": "银行业务",
        "securities": "证券/基金业务",
        "insurance": "保险业务",
        "payment": "支付业务",
    }

    def get_scenarios(self):
        return list(self.SCENARIOS.items())

    # ---- 银行业务检查项 ----

    def _bank_account_open(self, data: dict) -> CheckResult:
        """开户环节的告知同意"""
        has_privacy_notice = data.get("has_privacy_notice", False)
        has_separate_consent = data.get("has_separate_consent", False)
        consent_method = data.get("consent_method", "")
        sensitive_items = data.get("sensitive_items", [])

        issues = []
        if not has_privacy_notice:
            issues.append("未提供独立的隐私政策/个人信息告知")
        if not has_separate_consent:
            issues.append("未单独获取个人信息授权（与非必要服务捆绑）")
        if "biometric" in sensitive_items and not has_separate_consent:
            issues.append("人脸/指纹等生物识别信息未单独同意")
        if consent_method == "pre_checked":
            issues.append("同意方式为默认勾选，违反单独同意要求")

        passed = has_privacy_notice and has_separate_consent
        severity = "PASS" if passed else ("WARN" if has_privacy_notice else "FAIL")
        return CheckResult(
            "bank_account_open", "开户环节 - 告知同意检查",
            severity, passed,
            "；".join(issues) if issues else "开户告知同意合规",
            "提供独立隐私政策、对敏感信息单独获取同意、禁止默认勾选",
            "PIPL Art.17, 23; JR/T 0171 5.2"
        )

    def _bank_credit(self, data: dict) -> CheckResult:
        """信贷信息处理"""
        has_loan_authorization = data.get("has_loan_authorization", False)
        limits_info_scope = data.get("limits_info_scope", False)
        has_post_lending_notice = data.get("has_post_lending_notice", False)
        shares_with_third_party = data.get("shares_with_third_party", False)
        third_party_consent = data.get("third_party_consent", False)

        issues = []
        if not has_loan_authorization:
            issues.append("未获取信贷信息处理授权")
        if not limits_info_scope:
            issues.append("信息收集范围超出信贷业务必需")
        if not has_post_lending_notice:
            issues.append("贷后管理中的信息使用未充分告知")
        if shares_with_third_party and not third_party_consent:
            issues.append("向第三方（担保/催收/评估）共享信息未单独授权")

        passed = has_loan_authorization and limits_info_scope
        severity = "PASS" if passed else "FAIL"
        return CheckResult(
            "bank_credit", "信贷业务 - 个人信息处理合规",
            severity, passed,
            "；".join(issues) if issues else "信贷信息处理合规",
            "明确授权范围、遵循最小必要、第三方共享需单独同意",
            "PIPL Art.6, 17, 23"
        )

    def _bank_credit_report(self, data: dict) -> CheckResult:
        """征信查询与报送"""
        has_authorization = data.get("has_authorization", False)
        has_purpose_limitation = data.get("has_purpose_limitation", False)
        has_dispute_mechanism = data.get("has_dispute_mechanism", False)
        query_frequency = data.get("query_frequency", "normal")

        issues = []
        if not has_authorization:
            issues.append("未获得征信查询授权书")
        if not has_purpose_limitation:
            issues.append("征信信息使用目的不明确（如贷后管理 vs 贷前审批混用）")
        if not has_dispute_mechanism:
            issues.append("未建立征信异议处理机制")
        if query_frequency != "normal":
            issues.append("征信查询频率异常，存在越权查询\风险")

        passed = has_authorization and has_purpose_limitation
        severity = "PASS" if passed else "FAIL"
        return CheckResult(
            "bank_credit_report", "征信信息 - 查询与报送合规",
            severity, passed,
            "；".join(issues) if issues else "征信管理合规",
            "取得书面授权、限定查询用途、建立异议处理机制",
            "《征信业管理条例》Art.18, 19, 25"
        )

    def _bank_marketing(self, data: dict) -> CheckResult:
        """信用卡营销"""
        has_marketing_consent = data.get("has_marketing_consent", False)
        opt_out_available = data.get("opt_out_available", False)
        uses_push_notification = data.get("uses_push_notification", False)
        shares_for_marketing = data.get("shares_for_marketing", False)

        issues = []
        if not has_marketing_consent:
            issues.append("营销推广未获得用户同意")
        if not opt_out_available:
            issues.append("未提供便捷的退订/拒绝渠道")
        if uses_push_notification and not opt_out_available:
            issues.append("推送通知无关闭选项")
        if shares_for_marketing:
            issues.append("将个人信息用于第三方营销共享，需单独同意")

        passed = has_marketing_consent and opt_out_available
        severity = "PASS" if passed else "WARN"
        return CheckResult(
            "bank_marketing", "信用卡营销 - 个人信息使用合规",
            severity, passed,
            "；".join(issues) if issues else "营销合规",
            "获取营销同意、提供便捷退订、第三方共享需单独授权",
            "PIPL Art.24; 《金融消费者权益保护实施办法》Art.16, 21"
        )

    def _bank_data_share(self, data: dict) -> CheckResult:
        """账户信息共享"""
        group_sharing = data.get("group_sharing", False)
        group_notice = data.get("group_notice", False)
        third_party_sharing = data.get("third_party_sharing", False)
        third_party_consent = data.get("third_party_consent", False)

        issues = []
        if group_sharing and not group_notice:
            issues.append("集团内共享个人金融信息未充分告知用户")
        if third_party_sharing and not third_party_consent:
            issues.append("向第三方提供个人金融信息未单独同意")
        if group_sharing:
            issues.append("建议在隐私政策中明确列明集团共享的接收方范围")

        passed = not (group_sharing and not group_notice) and not (third_party_sharing and not third_party_consent)
        severity = "PASS" if passed else "FAIL"
        return CheckResult(
            "bank_data_share", "账户信息共享 - 第三方与集团内部合规",
            severity, passed,
            "；".join(issues) if issues else "信息共享合规",
            "集团共享需告知、第三方提供需单独同意",
            "PIPL Art.21, 23; JR/T 0171 6.2"
        )

    def _bank_data_classification(self, data: dict) -> CheckResult:
        """个人金融信息分类分级"""
        has_classification = data.get("has_classification", False)
        c3_protection = data.get("c3_protection", False)
        c2_protection = data.get("c2_protection", False)
        has_data_map = data.get("has_data_map", False)

        issues = []
        if not has_classification:
            issues.append("未按 JR/T 0197 建立金融数据分类分级制度")
        if not has_data_map:
            issues.append("未建立个人金融信息数据资产地图")
        if not c3_protection:
            issues.append("C3 类信息（账户鉴别信息）安全保护措施不足")
        if not c2_protection:
            issues.append("C2 类信息（可识别身份信息）安全保护措施不足")

        passed = has_classification and c3_protection
        severity = "PASS" if passed else "FAIL"
        return CheckResult(
            "bank_data_classification", "个人金融信息 - 分类分级合规",
            severity, passed,
            "；".join(issues) if issues else "分类分级合规",
            "按 JR/T 0197 完成分类分级，C3类信息重点保护",
            "JR/T 0197 5.2; JR/T 0171 4.2"
        )

    def _bank_automated_decision(self, data: dict) -> CheckResult:
        """自动化决策"""
        uses_auto_decision = data.get("uses_auto_decision", False)
        has_disclosure = data.get("has_disclosure", False)
        opt_out_available = data.get("opt_out_available", False)
        has_explanation = data.get("has_explanation", False)

        if not uses_auto_decision:
            return CheckResult(
                "bank_automated_decision", "自动化决策 - 合规检查",
                "PASS", True, "未使用自动化决策", "", "PIPL Art.24, 73"
            )

        issues = []
        if not has_disclosure:
            issues.append("未告知自动化决策的逻辑、目的和影响")
        if not opt_out_available:
            issues.append("未提供拒绝仅通过自动化决策方式作出决定的权利")
        if not has_explanation:
            issues.append("未提供自动化决策结果的解释说明机制")

        passed = has_disclosure and opt_out_available
        severity = "PASS" if passed else "FAIL"
        return CheckResult(
            "bank_automated_decision", "自动化决策 - 合规检查",
            severity, passed,
            "；".join(issues) if issues else "自动化决策合规",
            "告知逻辑与影响、提供拒绝权、支持解释说明",
            "PIPL Art.24, 73"
        )

    def _bank_data_retention(self, data: dict) -> CheckResult:
        """数据留存与删除"""
        has_retention_policy = data.get("has_retention_policy", False)
        auto_delete = data.get("auto_delete", False)
        account_cancellation = data.get("account_cancellation", False)
        can_request_delete = data.get("can_request_delete", False)

        issues = []
        if not has_retention_policy:
            issues.append("未制定个人信息留存期限制度")
        if not auto_delete:
            issues.append("未设置到期自动删除/匿名化机制")
        if not account_cancellation:
            issues.append("账户注销后个人信息未同步删除")
        if not can_request_delete:
            issues.append("未提供用户主动删除个人信息的渠道")

        passed = has_retention_policy and account_cancellation
        severity = "PASS" if passed else "WARN"
        return CheckResult(
            "bank_data_retention", "数据留存与删除 - 合规检查",
            severity, passed,
            "；".join(issues) if issues else "数据留存合规",
            "短留存期限、到期自动处置、注销即删除",
            "PIPL Art.19, 47"
        )

    # ---- 证券/基金业务检查项 ----

    def _sec_suitability(self, data: dict) -> CheckResult:
        """适当性管理"""
        kyc_scope_reasonable = data.get("kyc_scope_reasonable", False)
        has_privacy_notice = data.get("has_privacy_notice", False)
        kyc_retention_limited = data.get("kyc_retention_limited", False)

        issues = []
        if not kyc_scope_reasonable:
            issues.append("KYC信息收集范围超出适当性管理必需")
        if not has_privacy_notice:
            issues.append("KYC信息收集未充分告知用途")
        if not kyc_retention_limited:
            issues.append("KYC信息留存期限未明确限定")

        passed = kyc_scope_reasonable and has_privacy_notice
        severity = "PASS" if passed else "WARN"
        return CheckResult(
            "sec_suitability", "适当性管理 - KYC信息收集合规",
            severity, passed,
            "；".join(issues) if issues else "适当性管理合规",
            "KYC信息收集最小必要、告知用途、限定留存",
            "PIPL Art.6; 《证券期货投资者适当性管理办法》Art.6"
        )

    def _sec_trade_info(self, data: dict) -> CheckResult:
        """交易信息保护"""
        encrypt_transmission = data.get("encrypt_transmission", False)
        access_control = data.get("access_control", False)
        log_audit = data.get("log_audit", False)

        issues = []
        if not encrypt_transmission:
            issues.append("交易信息传输未加密")
        if not access_control:
            issues.append("交易信息访问权限控制不足")
        if not log_audit:
            issues.append("交易信息访问日志不完整")

        passed = encrypt_transmission and access_control
        severity = "PASS" if passed else "FAIL"
        return CheckResult(
            "sec_trade_info", "交易信息 - 安全保护合规",
            severity, passed,
            "；".join(issues) if issues else "交易信息安全保护合规",
            "加密传输、严格权限控制、完整审计日志",
            "PIPL Art.6, 51; JR/T 0171 5.3"
        )

    def _sec_investor_share(self, data: dict) -> CheckResult:
        """投资者信息共享"""
        csdc_sharing = data.get("csdc_sharing", False)
        csdc_notice = data.get("csdc_notice", False)
        custodian_sharing = data.get("custodian_sharing", False)
        custodian_notice = data.get("custodian_notice", False)

        issues = []
        if csdc_sharing and not csdc_notice:
            issues.append("向中国结算报送信息未充分告知投资者")
        if custodian_sharing and not custodian_notice:
            issues.append("向托管银行传输信息未告知投资者")

        passed = not (csdc_sharing and not csdc_notice)
        severity = "PASS" if passed else "WARN"
        return CheckResult(
            "sec_investor_share", "投资者信息 - 登记结算共享合规",
            severity, passed,
            "；".join(issues) if issues else "信息共享合规",
            "明确告知信息共享的必要性和接收方",
            "PIPL Art.17, 23"
        )

    def _sec_robo_advisor(self, data: dict) -> CheckResult:
        """智能投顾"""
        has_algorithm_filing = data.get("has_algorithm_filing", False)
        has_risk_warning = data.get("has_risk_warning", False)
        has_human_override = data.get("has_human_override", False)

        issues = []
        if not has_algorithm_filing:
            issues.append("算法推荐服务未备案")
        if not has_risk_warning:
            issues.append("智能投顾建议未提示算法风险")
        if not has_human_override:
            issues.append("未提供人工投顾替代选项")

        passed = has_algorithm_filing and has_risk_warning
        severity = "PASS" if passed else "WARN"
        return CheckResult(
            "sec_robo_advisor", "智能投顾 - 自动化决策合规",
            severity, passed,
            "；".join(issues) if issues else "智能投顾合规",
            "算法备案、风险提示、提供人工替代",
            "PIPL Art.24; 《互联网信息服务算法推荐管理规定》"
        )

    # ---- 保险业务检查项 ----

    def _ins_underwriting(self, data: dict) -> CheckResult:
        """核保健康信息"""
        info_collection_reasonable = data.get("info_collection_reasonable", False)
        has_separate_consent = data.get("has_separate_consent", False)
        third_party_verification = data.get("third_party_verification", False)
        third_party_consent = data.get("third_party_consent", False)

        issues = []
        if not info_collection_reasonable:
            issues.append("健康告知问题超出核保必需范围")
        if not has_separate_consent:
            issues.append("健康信息（敏感个人信息）未取得单独同意")
        if third_party_verification and not third_party_consent:
            issues.append("委托第三方（体检/调查公司）验证信息未单独授权")

        passed = info_collection_reasonable and has_separate_consent
        severity = "PASS" if passed else "FAIL"
        return CheckResult(
            "ins_underwriting", "核保环节 - 健康信息收集合规",
            severity, passed,
            "；".join(issues) if issues else "核保信息收集合规",
            "信息收集最小必要、敏感信息单独同意、第三方授权",
            "PIPL Art.28, 29; 《保险法》Art.16"
        )

    def _ins_claim(self, data: dict) -> CheckResult:
        """理赔调查"""
        notice_purpose = data.get("notice_purpose", False)
        scope_limited = data.get("scope_limited", False)
        third_party_investigation = data.get("third_party_investigation", False)
        authorization_scope = data.get("authorization_scope", False)

        issues = []
        if not notice_purpose:
            issues.append("理赔调查目的未告知被调查人")
        if not scope_limited:
            issues.append("调查范围超出理赔必需（如调查与出险无关的健康记录）")
        if third_party_investigation and not authorization_scope:
            issues.append("委托第三方调查的授权范围不明确")

        passed = notice_purpose and scope_limited
        severity = "PASS" if passed else "WARN"
        return CheckResult(
            "ins_claim", "理赔调查 - 个人信息收集合规",
            severity, passed,
            "；".join(issues) if issues else "理赔调查合规",
            "明示调查目的、限定调查范围、明确第三方授权",
            "PIPL Art.6, 17, 23"
        )

    def _ins_reinsurance(self, data: dict) -> CheckResult:
        """再保险信息共享"""
        has_reinsurance = data.get("has_reinsurance", False)
        has_notice = data.get("has_notice", False)
        cross_border = data.get("cross_border", False)
        cross_border_compliant = data.get("cross_border_compliant", False)

        if not has_reinsurance:
            return CheckResult(
                "ins_reinsurance", "再保险 - 信息共享合规",
                "PASS", True, "未涉及再保险安排", "", "PIPL Art.21, 23"
            )

        issues = []
        if not has_notice:
            issues.append("再保险安排中的个人信息共享未告知投保人")
        if cross_border and not cross_border_compliant:
            issues.append("跨境再保险数据未完成出境合规评估")

        passed = has_notice and not (cross_border and not cross_border_compliant)
        severity = "PASS" if passed else "WARN"
        return CheckResult(
            "ins_reinsurance", "再保险 - 信息共享合规",
            severity, passed,
            "；".join(issues) if issues else "再保险信息共享合规",
            "告知再保险信息共享、跨境数据需完成出境评估",
            "PIPL Art.21, 38"
        )

    # ---- 支付业务检查项 ----

    def _pay_transaction(self, data: dict) -> CheckResult:
        """交易信息最小必要"""
        collects_minimal = data.get("collects_minimal", False)
        no_extra_info = data.get("no_extra_info", False)
        has_notice = data.get("has_notice", False)

        issues = []
        if not collects_minimal:
            issues.append("交易信息收集超出支付必需范围（如收集通讯录、位置）")
        if not no_extra_info:
            issues.append("以风控名义过度收集非必要信息")
        if not has_notice:
            issues.append("交易信息收集未在隐私政策中明确告知")

        passed = collects_minimal and has_notice
        severity = "PASS" if passed else "FAIL"
        return CheckResult(
            "pay_transaction", "交易信息 - 最小必要原则合规",
            severity, passed,
            "；".join(issues) if issues else "交易信息最小必要合规",
            "仅收集交易必需信息、明确告知收集范围",
            "PIPL Art.6; JR/T 0171 5.1"
        )

    def _pay_risk_control(self, data: dict) -> CheckResult:
        """风控信息使用"""
        fraud_detection = data.get("fraud_detection", False)
        purpose_limited = data.get("purpose_limited", False)
        device_info_used = data.get("device_info_used", False)
        device_info_notice = data.get("device_info_notice", False)

        issues = []
        if fraud_detection and not purpose_limited:
            issues.append("风控数据用于营销等其他目的，超出原授权范围")
        if device_info_used and not device_info_notice:
            issues.append("设备信息（IMEI/OAID/IMSI）收集未告知")

        passed = not (fraud_detection and not purpose_limited)
        severity = "PASS" if passed else "WARN"
        return CheckResult(
            "pay_risk_control", "风控信息 - 使用目的合规",
            severity, passed,
            "；".join(issues) if issues else "风控信息使用合规",
            "风控数据不得用于营销、设备信息收集需告知",
            "PIPL Art.6, 17"
        )

    def _pay_tokenization(self, data: dict) -> CheckResult:
        """支付标记化"""
        uses_tokenization = data.get("uses_tokenization", False)
        pan_not_stored = data.get("pan_not_stored", False)
        token_scope_limited = data.get("token_scope_limited", False)

        if not uses_tokenization:
            return CheckResult(
                "pay_tokenization", "支付标记化 - 合规检查",
                "WARN", False,
                "未使用支付标记化技术，建议采用Tokenization替代直接处理卡号",
                "采用支付标记化（Tokenization）降低敏感信息暴露风险",
                "JR/T 0171 5.3; PCI DSS"
            )

        issues = []
        if not pan_not_stored:
            issues.append("系统仍直接存储完整卡号，未替换为令牌")
        if not token_scope_limited:
            issues.append("令牌使用范围未限定（如限定商户、渠道、金额）")

        passed = pan_not_stored and token_scope_limited
        severity = "PASS" if passed else "WARN"
        return CheckResult(
            "pay_tokenization", "支付标记化 - 合规检查",
            severity, passed,
            "；".join(issues) if issues else "支付标记化合规",
            "使用令牌替换卡号、限定令牌使用范围",
            "JR/T 0171 5.3"
        )

    # ---- 场景路由 ----

    def run(self, scenario: str, data: dict) -> List[CheckResult]:
        scenario = scenario.lower()
        results = []

        if scenario == "banking":
            results.append(self._bank_account_open(data))
            results.append(self._bank_credit(data))
            results.append(self._bank_credit_report(data))
            results.append(self._bank_marketing(data))
            results.append(self._bank_data_share(data))
            results.append(self._bank_data_classification(data))
            results.append(self._bank_automated_decision(data))
            results.append(self._bank_data_retention(data))

        elif scenario == "securities":
            results.append(self._sec_suitability(data))
            results.append(self._sec_trade_info(data))
            results.append(self._sec_investor_share(data))
            results.append(self._sec_robo_advisor(data))

        elif scenario == "insurance":
            results.append(self._ins_underwriting(data))
            results.append(self._ins_claim(data))
            results.append(self._ins_reinsurance(data))

        elif scenario == "payment":
            results.append(self._pay_transaction(data))
            results.append(self._pay_risk_control(data))
            results.append(self._pay_tokenization(data))

        else:
            raise ValueError(f"不支持的场景: {scenario}，可选: {', '.join(self.SCENARIOS.keys())}")

        return results


# ============================================================
# 交互式问答数据
# ============================================================

BANKING_QUESTIONS = [
    ("has_privacy_notice", "开户时是否提供独立的隐私政策/个人信息保护告知？(y/n): "),
    ("has_separate_consent", "个人信息授权是否单独获取（不与服务协议捆绑）？(y/n): "),
    ("consent_method", "同意方式是什么？（manual=手动勾选 / pre_checked=默认勾选）: "),
    ("sensitive_items", "是否收集人脸/指纹等生物识别信息？（如有，输入 biometric，否则留空）: "),
    ("has_loan_authorization", "信贷业务是否取得个人信息处理授权？(y/n): "),
    ("limits_info_scope", "信贷信息收集范围是否限于业务必需？(y/n): "),
    ("has_post_lending_notice", "贷后管理中的信息使用是否充分告知？(y/n): "),
    ("shares_with_third_party", "是否向第三方（担保/催收/评估）共享信贷信息？(y/n): "),
    ("third_party_consent", "第三方共享是否取得单独同意？(y/n): "),
    ("has_authorization", "征信查询是否有书面授权？(y/n): "),
    ("has_purpose_limitation", "征信信息使用目的是否明确限定？(y/n): "),
    ("has_dispute_mechanism", "是否建立征信异议处理机制？(y/n): "),
    ("query_frequency", "征信查询频率是否正常？（normal=正常 / abnormal=异常）: "),
    ("has_marketing_consent", "信用卡营销是否获得用户同意？(y/n): "),
    ("opt_out_available", "是否提供便捷的退订/拒绝渠道？(y/n): "),
    ("uses_push_notification", "是否使用推送通知进行营销？(y/n): "),
    ("shares_for_marketing", "是否将个人信息用于第三方营销共享？(y/n): "),
    ("group_sharing", "是否存在集团内信息共享安排？(y/n): "),
    ("group_notice", "集团共享是否已告知用户？(y/n): "),
    ("third_party_sharing", "是否向第三方提供个人金融信息？(y/n): "),
    ("has_classification", "是否按 JR/T 0197 完成数据分类分级？(y/n): "),
    ("has_data_map", "是否建立个人金融信息数据资产地图？(y/n): "),
    ("c3_protection", "C3类信息（账户鉴别信息）是否有安全保护措施？(y/n): "),
    ("c2_protection", "C2类信息（可识别身份信息）是否有安全保护措施？(y/n): "),
    ("uses_auto_decision", "是否使用自动化决策（如授信模型）？(y/n): "),
    ("has_disclosure", "自动化决策的逻辑和影响是否告知用户？(y/n): "),
    ("has_explanation", "是否提供自动化决策结果的解释说明？(y/n): "),
    ("has_retention_policy", "是否制定个人信息留存期限制度？(y/n): "),
    ("auto_delete", "是否设置到期自动删除/匿名化机制？(y/n): "),
    ("account_cancellation", "账户注销后个人信息是否同步删除？(y/n): "),
    ("can_request_delete", "是否提供用户主动删除个人信息的渠道？(y/n): "),
]

SECURITIES_QUESTIONS = [
    ("kyc_scope_reasonable", "KYC信息收集范围是否限于适当性管理必需？(y/n): "),
    ("has_privacy_notice", "KYC信息的收集用途是否告知投资者？(y/n): "),
    ("kyc_retention_limited", "KYC信息留存期限是否明确限定？(y/n): "),
    ("encrypt_transmission", "交易信息传输是否加密？(y/n): "),
    ("access_control", "交易信息访问是否有权限控制？(y/n): "),
    ("log_audit", "交易信息访问日志是否完整？(y/n): "),
    ("csdc_sharing", "是否向中国结算报送投资者信息？(y/n): "),
    ("csdc_notice", "投资者是否知晓信息报送中国结算？(y/n): "),
    ("custodian_sharing", "是否向托管银行传输投资者信息？(y/n): "),
    ("custodian_notice", "投资者是否知晓信息传输托管银行？(y/n): "),
    ("has_algorithm_filing", "算法推荐服务是否完成备案？(y/n): "),
    ("has_risk_warning", "智能投顾建议是否提示算法风险？(y/n): "),
    ("has_human_override", "是否提供人工投顾替代选项？(y/n): "),
]

INSURANCE_QUESTIONS = [
    ("info_collection_reasonable", "健康告知问题是否限于核保必需范围？(y/n): "),
    ("has_separate_consent", "健康信息（敏感信息）是否取得单独同意？(y/n): "),
    ("third_party_verification", "是否委托第三方（体检/调查公司）进行核保验证？(y/n): "),
    ("third_party_consent", "第三方验证是否取得投保人单独授权？(y/n): "),
    ("notice_purpose", "理赔调查目的是否告知被调查人？(y/n): "),
    ("scope_limited", "调查范围是否限于理赔必需？(y/n): "),
    ("third_party_investigation", "是否委托第三方进行理赔调查？(y/n): "),
    ("authorization_scope", "第三方理赔调查的授权范围是否明确？(y/n): "),
    ("has_reinsurance", "是否涉及再保险安排？(y/n): "),
    ("has_notice", "再保险信息共享是否告知投保人？(y/n): "),
    ("cross_border", "再保险是否涉及跨境数据传输？(y/n): "),
    ("cross_border_compliant", "跨境数据是否完成出境合规评估？(y/n): "),
]

PAYMENT_QUESTIONS = [
    ("collects_minimal", "交易信息是否限于支付必需（不收集通讯录/位置等）？(y/n): "),
    ("no_extra_info", "是否以风控名义过度收集非必要信息？(y/n): "),
    ("has_notice", "交易信息收集是否在隐私政策中明确告知？(y/n): "),
    ("fraud_detection", "是否使用风控数据用于反欺诈检测？(y/n): "),
    ("purpose_limited", "风控数据是否限定用于安全目的（不用于营销）？(y/n): "),
    ("device_info_used", "是否收集设备信息（IMEI/OAID/IMSI）？(y/n): "),
    ("device_info_notice", "设备信息收集是否告知用户？(y/n): "),
    ("uses_tokenization", "是否使用支付标记化技术（Tokenization）？(y/n): "),
    ("pan_not_stored", "系统是否不存储完整卡号（已替换为令牌）？(y/n): "),
    ("token_scope_limited", "令牌使用范围是否限定（商户/渠道/金额）？(y/n): "),
]

SCENARIO_QUESTIONS = {
    "banking": BANKING_QUESTIONS,
    "securities": SECURITIES_QUESTIONS,
    "insurance": INSURANCE_QUESTIONS,
    "payment": PAYMENT_QUESTIONS,
}


def interactive_input(scenario: str) -> dict:
    """交互式问答"""
    data = {}
    questions = SCENARIO_QUESTIONS.get(scenario, [])

    print(f"\n{'='*50}")
    print(f"📋 {FinPIPLChecker.SCENARIOS.get(scenario, scenario)} — 合规自查")
    print(f"{'='*50}")
    print("（输入 y/n 或按提示输入，直接回车默认为 n/留空）\n")

    for key, prompt in questions:
        raw = input(prompt).strip().lower()
        if key == "consent_method":
            data[key] = "pre_checked" if raw == "pre_checked" else "manual" if raw == "manual" else ""
        elif key == "query_frequency":
            data[key] = "normal" if raw == "normal" else "abnormal" if raw in ("abnormal", "异常") else "normal"
        elif key == "sensitive_items":
            data[key] = ["biometric"] if "biometric" in raw or "人脸" in raw or "指纹" in raw else []
        else:
            data[key] = raw.startswith("y")

    return data


# ============================================================
# 报告生成
# ============================================================

def generate_report_markdown(report: CheckReport) -> str:
    """生成 Markdown 格式报告"""
    lines = []
    lines.append(f"# 🏦 Fin-PIPL 合规检查报告\n")
    lines.append(f"**工具版本**: {report.version}  ")
    lines.append(f"**检查时间**: {report.timestamp}  ")
    lines.append(f"**检查场景**: {FinPIPLChecker.SCENARIOS.get(report.scenario, report.scenario)}  ")
    lines.append(f"**检查项**: {report.summary['total']} 项  ")
    lines.append(f"**合规率**: {report.summary['pass_rate']:.0f}%\n")

    lines.append("## 📊 总体结果\n")
    lines.append(f"- ✅ 通过: {report.summary['passed']} 项")
    lines.append(f"- ⚠️ 警告: {report.summary['warnings']} 项")
    lines.append(f"- ❌ 未通过: {report.summary['failed']} 项\n")

    lines.append("## 📋 详细检查结果\n")
    for item in report.items:
        status_icon = "✅" if item["passed"] else ("❌" if item["severity"] == "FAIL" else "⚠️")
        lines.append(f"### {status_icon} {item['description']}")
        lines.append(f"**状态**: {item['severity']}  ")
        lines.append(f"**详情**: {item['details']}  ")
        lines.append(f"**建议**: {item['recommendation']}  ")
        lines.append(f"**法规依据**: {item['regulation_ref']}  ")
        lines.append("")

    lines.append("---")
    lines.append(f"*本报告由 Fin-PIPL v{report.version} 自动生成，仅供参考，不构成法律意见。*")
    return "\n".join(lines)


def generate_report_html(report: CheckReport) -> str:
    """生成 HTML 格式报告"""
    items_html = ""
    for item in report.items:
        sev_color = {"PASS": "#27ae60", "WARN": "#f39c12", "FAIL": "#e74c3c"}
        color = sev_color.get(item["severity"], "#333")
        icon = "&#10004;" if item["passed"] else ("&#10008;" if item["severity"] == "FAIL" else "&#9888;")
        items_html += f"""
        <div class="check-item">
            <div class="check-header" style="border-left: 4px solid {color};">
                <span class="check-icon" style="color: {color};">{icon}</span>
                <span class="check-title">{item['description']}</span>
                <span class="check-status" style="background: {color}20; color: {color};">{item['severity']}</span>
            </div>
            <div class="check-body">
                <p><strong>详情：</strong>{item['details']}</p>
                <p><strong>建议：</strong>{item['recommendation']}</p>
                <p><strong>法规依据：</strong>{item['regulation_ref']}</p>
            </div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>Fin-PIPL 合规检查报告</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; color: #333; line-height: 1.6; }}
h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
.summary {{ display: flex; gap: 20px; margin: 20px 0; }}
.summary-card {{ background: #f8f9fa; border-radius: 8px; padding: 20px; flex: 1; text-align: center; }}
.summary-card.pass {{ border-top: 3px solid #27ae60; }}
.summary-card.warn {{ border-top: 3px solid #f39c12; }}
.summary-card.fail {{ border-top: 3px solid #e74c3c; }}
.num {{ font-size: 2em; font-weight: bold; }}
.pass .num {{ color: #27ae60; }}
.warn .num {{ color: #f39c12; }}
.fail .num {{ color: #e74c3c; }}
.check-item {{ background: #fff; border: 1px solid #eee; border-radius: 8px; margin: 10px 0; overflow: hidden; }}
.check-header {{ padding: 12px 16px; display: flex; align-items: center; gap: 10px; cursor: default; }}
.check-icon {{ font-size: 1.2em; }}
.check-title {{ flex: 1; font-weight: 500; }}
.check-status {{ padding: 2px 10px; border-radius: 12px; font-size: 0.8em; font-weight: 600; }}
.check-body {{ padding: 0 16px 12px; color: #555; font-size: 0.95em; }}
.footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; font-size: 0.85em; color: #999; }}
</style></head><body>
<h1>🏦 Fin-PIPL 合规检查报告</h1>
<p><strong>工具版本：</strong>{report.version} &nbsp;|&nbsp; <strong>检查时间：</strong>{report.timestamp} &nbsp;|&nbsp; <strong>检查场景：</strong>{FinPIPLChecker.SCENARIOS.get(report.scenario, report.scenario)}</p>
<div class="summary">
<div class="summary-card pass"><div class="num">{report.summary['passed']}</div><div>通过</div></div>
<div class="summary-card warn"><div class="num">{report.summary['warnings']}</div><div>警告</div></div>
<div class="summary-card fail"><div class="num">{report.summary['failed']}</div><div>未通过</div></div>
</div>
{items_html}
<div class="footer">本报告由 Fin-PIPL v{report.version} 自动生成，仅供参考，不构成法律意见。</div>
</body></html>"""


# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Fin-PIPL — 金融行业个人信息保护合规检查工具"
    )
    parser.add_argument(
        "--scenario", "-s",
        choices=["banking", "securities", "insurance", "payment"],
        default="banking",
        help="检查场景：banking(银行), securities(证券), insurance(保险), payment(支付)"
    )
    parser.add_argument(
        "--output", "-o",
        help="输出文件路径"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["markdown", "json", "html"],
        default="markdown",
        help="输出格式（默认 markdown）"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="交互式问答模式"
    )
    parser.add_argument(
        "--list-scenarios",
        action="store_true",
        help="列出支持的业务场景"
    )
    parser.add_argument(
        "--version", "-V",
        action="version",
        version="Fin-PIPL v1.0.0"
    )

    args = parser.parse_args()

    if args.list_scenarios:
        print("Fin-PIPL 支持的场景：")
        for key, name in FinPIPLChecker.SCENARIOS.items():
            print(f"  {key:15s} - {name}")
        return

    # 交互式问答
    if args.interactive:
        data = interactive_input(args.scenario)
    else:
        data = {}

    # 执行检查
    checker = FinPIPLChecker()
    results = checker.run(args.scenario, data)

    # 统计
    passed = sum(1 for r in results if r.severity == "PASS")
    warnings = sum(1 for r in results if r.severity == "WARN")
    failed = sum(1 for r in results if r.severity == "FAIL")
    total = len(results)

    report = CheckReport(
        tool_name="fin-pipl",
        version="1.0.0",
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        scenario=args.scenario,
        summary={
            "total": total, "passed": passed, "warnings": warnings,
            "failed": failed, "pass_rate": (passed / total * 100) if total else 0
        },
        items=[asdict(r) for r in results],
    )

    # 控制台输出
    print(f"\n{'='*50}")
    print(f"🏦 Fin-PIPL 合规检查报告")
    print(f"{'='*50}")
    print(f"场景: {FinPIPLChecker.SCENARIOS.get(args.scenario, args.scenario)}")
    print(f"时间: {report.timestamp}")
    print(f"结果: {passed}/{total} 通过, {warnings} 警告, {failed} 未通过")
    print(f"合规率: {report.summary['pass_rate']:.0f}%\n")

    for r in results:
        icon = "✅" if r.passed else ("⚠️" if r.severity == "WARN" else "❌")
        print(f"  {icon} {r.description}")
        if r.details:
            print(f"    详情: {r.details}")
        if not r.passed:
            print(f"    建议: {r.recommendation}")

    # 文件输出
    if args.output:
        if args.format == "json":
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)
        elif args.format == "html":
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(generate_report_html(report))
        else:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(generate_report_markdown(report))
        print(f"\n✅ 报告已保存到: {args.output}")


if __name__ == "__main__":
    main()

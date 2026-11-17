#!/usr/bin/env python3
"""CCPA 护栏规则包 (ccpa)。

覆盖《加州消费者隐私法案》(CCPA/CPRA) 语境下的个人数据类别。
纯数据定义，无副作用、无网络、无动态执行。
字段定义与通用内核一致：
    PATTERNS: (id, regex, label, category, severity, validate, mask)
    KEYWORDS: (keyword, label, category, severity)
"""

PROFILE = {
    "id": "ccpa",
    "name": "CCPA 护栏规则",
    "version": "1.0.0",
    "basis": "CCPA (Cal. Civ. Code § 1798.100 et seq.)、CPRA 2023",
}

PATTERNS = [
    # —— 通用（所有法域）——
    ("email",
     r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}",
     "Email address", "Contact", "medium", None, "partial"),
    ("ipv4",
     r"(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)",
     "IPv4 address", "Network identifier", "low", "ipv4", "partial"),
    ("mac_addr",
     r"(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}",
     "MAC address", "Network identifier", "low", None, "partial"),

    # —— US/CA 联系方式 ——
    ("us_phone",
     r"1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
     "US phone number (NANPA)", "Contact", "high", None, "partial"),

    # —— 金融 ——
    ("credit_card",
     r"(?:4\d{3}|5[1-5]\d{2}|3[47]\d{2}|6011|65\d{2})\d{10,15}",
     "Credit card number (Luhn)", "Financial", "high", "luhn", "partial"),
    ("us_bank_routing",
     r"\b\d{9}\b",
     "US bank routing number", "Financial", "medium", None, "partial"),

    # —— 身份标识 ——
    ("ssn",
     r"(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0000)\d{4}",
     "US Social Security Number (SSN)", "National identifier", "high", None, "full"),
    ("us_passport",
     r"\b\d{9}\b",
     "US passport number (9-digit)", "National identifier", "high", None, "full"),
    ("ca_driver_license",
     r"[A-Za-z]\d{7}",
     "California Driver License number", "State identifier", "high", None, "partial"),
    ("ca_id_card",
     r"\d{9}",
     "California ID card number", "State identifier", "high", None, "partial"),
]

KEYWORDS = [
    # CCPA § 1798.140(v)(2) Sensitive PI (CPRA 2023)
    ("social security", "Sensitive PI — SSN indicator", "Sensitive PI", "high"),
    ("driver's license", "Sensitive PI — DL indicator", "Sensitive PI", "high"),
    ("passport number", "Sensitive PI — passport indicator", "Sensitive PI", "high"),

    # Commercial information (CCPA § 1798.140(A)(D))
    ("purchase history", "Commercial information", "Commercial", "medium"),
    ("transaction history", "Commercial information", "Commercial", "medium"),
    ("credit score", "Commercial / consumer reporting", "Commercial", "high"),

    # Protected classifications
    ("race", "Protected classification", "Protected class", "high"),
    ("ethnicity", "Protected classification", "Protected class", "high"),
    ("disability", "Protected classification", "Protected class", "high"),
    ("medical condition", "Protected classification — medical", "Protected class", "high"),

    # Geolocation
    ("geolocation", "Precise geolocation (CPRA)", "Geolocation", "high"),
    ("gps coordinates", "Precise geolocation (CPRA)", "Geolocation", "high"),

    # Biometric
    ("biometric data", "Biometric information", "Biometric", "high"),
    ("fingerprint", "Biometric information", "Biometric", "high"),
    ("facial recognition", "Biometric information", "Biometric", "high"),

    # Internet activity
    ("browsing history", "Internet/electronic network activity", "Internet activity", "medium"),
    ("search history", "Internet/electronic network activity", "Internet activity", "medium"),

    # Employment / Education
    ("employment history", "Employment-related information", "Employment", "medium"),
    ("education record", "Education information", "Education", "medium"),
]

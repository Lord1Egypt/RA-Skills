"""Email category definitions for classification."""

from enum import Enum


class EmailCategory(str, Enum):
    """Predefined email categories for classification."""
    VERIFICATION = "verification"  # Verification codes, account confirmations, activation links
    SECURITY = "security"          # Security alerts, login notifications, password changes
    TRANSACTIONAL = "transactional"  # Receipts, order confirmations, shipping notices
    PROMOTION = "promotion"        # Marketing emails, promotions, rewards (legitimate)
    SUBSCRIPTION = "subscription"  # Newsletters, digests, regular updates
    SPAM_LIKE = "spam_like"        # Likely spam or low-priority promotional
    NORMAL = "normal"              # Regular personal/business email


# Keywords for category detection (subject-only matching)
# More specific keywords should come first
CATEGORY_KEYWORDS = {
    EmailCategory.VERIFICATION: [
        # Chinese - 验证码相关（具体短语优先，避免单字太宽泛）
        "验证码是", "验证码：", "您的验证码", "验证码为",
        "校验码是", "校验码：", "您的校验码", "校验码为",
        "动态码是", "动态码：", "您的动态码",
        "一次性密码", "一次性验证",
        "短信验证码", "邮箱验证码", "安全验证码", "登录验证码", "身份验证码",
        # Chinese - 动作短语
        "验证您的", "确认您的邮箱", "激活您的账户",
        "请验证", "请确认邮箱", "请激活账户",
        # Chinese - 链接验证
        "确认链接", "激活链接", "验证链接", "点击验证", "点击激活",
        # Chinese - 绑定相关
        "绑定邮箱", "绑定手机", "绑定账户", "绑定账号", "邮箱绑定", "手机绑定",
        "帐号绑定", "账户绑定",
        # Chinese - 核心关键词（放在最后作为兜底）
        "验证码", "校验码", "激活码",
        # English - verification codes（具体短语优先）
        "verification code", "verification code is", "your verification code",
        "verify code", "verify your email", "verify your account",
        "confirmation code", "confirmation code is", "your confirmation code",
        "confirm code", "confirm your email", "confirm your account",
        "activation code", "activation code is", "your activation code",
        "activate code", "activate your email", "activate your account",
        "security code", "security code is", "your security code",
        "login code", "auth code", "authentication code",
        "one-time password", "one-time code", "one time password", "OTP",
        "your code is", "enter code", "use code", "code is",
        # English - verification links
        "click to verify", "click to confirm", "click to activate",
        "verify your email", "confirm your email", "activate your account",
        # English - 核心关键词（放在最后作为兜底）
        "activate", "activation",
    ],
    EmailCategory.SECURITY: [
        # Chinese
        "安全提醒", "安全警告", "账户安全", "登录提醒", "登录警告",
        "新设备登录", "异地登录", "可疑登录", "异常登录",
        "密码修改", "密码重置", "密码变更", "修改密码",
        "双重验证", "两步验证", "二次验证",
        # English
        "security alert", "security warning", "security notice",
        "login attempt", "new login", "unusual login", "suspicious login",
        "new device", "unrecognized device",
        "password change", "password reset", "change your password",
        "two-factor", "2FA", "two-step verification",
        "unusual activity", "account compromise", "account security",
        "protect your account", "secure your account",
    ],
    EmailCategory.TRANSACTIONAL: [
        # Chinese
        "订单确认", "订单详情", "发货通知", "快递通知", "物流信息",
        "支付成功", "支付通知", "付款成功", "收款通知",
        "收据", "发票", "账单", "交易通知",
        # English
        "order confirmation", "order details", "order #", "order number",
        "shipping notification", "shipped", "delivery", "tracking number",
        "payment confirmation", "payment received", "receipt", "invoice",
        "transaction", "purchase confirmation", "your order",
    ],
    EmailCategory.PROMOTION: [
        # Chinese - 正规营销推广（区别于 spam）
        "奖励", "福利", "优惠", "优惠券", "折扣", "促销",
        "领取", "立即领取", "点击领取", "限时", "抢购",
        "会员专享", "积分", "返现", "红包", "礼包",
        "活动", "促销活动", "优惠活动", "新品上市",
        "USDT", "BTC", "ETH",  # 加密货币交易所推广
        # English
        "reward", "bonus", "promo", "promotion", "discount", "sale",
        "claim your", "get your", "exclusive offer", "limited offer",
        "member benefit", "points", "cashback", "gift",
        "special promotion", "new arrival", "flash sale",
    ],
    EmailCategory.SUBSCRIPTION: [
        # Chinese
        "订阅", "退订", "取消订阅", "周刊", "日报", "周报",
        "每日推送", "每周推送", "新闻速递", "最新动态",
        # English
        "newsletter", "unsubscribe", "opt-out", "opt out",
        "weekly digest", "daily digest", "daily update", "weekly update",
        "subscription", "your subscription",
    ],
    EmailCategory.SPAM_LIKE: [
        # Chinese
        "恭喜您", "中奖", "免费领取", "限时优惠", "最后机会",
        "点击领取", "立即领取", "马上行动",
        # English
        "winner", "congratulations", "you've won", "you have won",
        "click here now", "act now", "limited time", "last chance",
        "exclusive offer", "special offer", "claim your",
    ],
}


def detect_category(subject: str, body: str = "") -> EmailCategory:
    """Detect email category based on subject line keywords.
    
    Args:
        subject: Email subject line (primary classification source)
        body: Email body (currently unused, reserved for future ML)
    
    Returns:
        EmailCategory enum value
    """
    # Use subject only for classification
    text = subject.lower()
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text:
                return category
    
    return EmailCategory.NORMAL

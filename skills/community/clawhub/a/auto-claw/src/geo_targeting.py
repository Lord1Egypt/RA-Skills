"""
GEO Targeting — WordPress 地理位置动态内容系统
基于用户地理位置显示不同内容：货币/语言/本地化信息/区域定价
"""
import re
import json
import hashlib
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime

# ============ 数据结构 ============

@dataclass
class GeoLocation:
    """地理位置信息"""
    country_code: str = ""      # ISO 3166-1 alpha-2: US, CN, DE, GB...
    country_name: str = ""
    region: str = ""            # 州/省
    city: str = ""
    city_lat: float = 0.0
    city_lng: float = 0.0
    currency: str = "USD"
    currency_symbol: str = "$"
    timezone: str = "UTC"
    locale: str = "en-US"
    is_eu: bool = False  # 欧盟用户（GDPR相关）
    ip_address: str = ""

@dataclass
class GeoVariant:
    """地理内容变体"""
    variant_id: str
    name: str
    countries: List[str] = field(default_factory=list)  # 国家代码白名单
    exclude_countries: List[str] = field(default_factory=list)  # 排除
    regions: List[str] = field(default_factory=list)
    currencies: List[str] = field(default_factory=list)
    is_default: bool = False

    # 内容覆盖
    headline: str = ""
    subheadline: str = ""
    cta_text: str = ""
    cta_url: str = ""
    price_display: str = ""  # 显示用价格 "$99" / "€89" / "¥699"
    local_price: float = 0.0

    # 本地化内容
    testimonial: str = ""  # 本地化推荐语
    badge: str = ""        # "🇩🇪 Lieferung in 2 Tagen" / "🇨🇳 中文支持"
    urgency_msg: str = ""  # "Nur noch 3 auf Lager!"

    # 附加内容
    extra_blocks: Dict[str, str] = field(default_factory=dict)  # name -> HTML


@dataclass
class CampaignConfig:
    """大促配置"""
    name: str
    start_time: datetime
    end_time: datetime
    variants: List[GeoVariant] = field(default_factory=list)
    default_variant: str = ""
    active: bool = True

# ============ IP解析 ============

class IPLookup:
    """IP到地理位置的解析"""

    # 内置简化版GeoIP映射（生产环境应使用MaxMind GeoLite2）
    # 格式：country_code -> country_name, currency, locale
    COUNTRY_DATA = {
        "US": {"name": "United States", "currency": "USD", "symbol": "$", "locale": "en-US", "eu": False},
        "CN": {"name": "China", "currency": "CNY", "symbol": "¥", "locale": "zh-CN", "eu": False},
        "DE": {"name": "Germany", "currency": "EUR", "symbol": "€", "locale": "de-DE", "eu": True},
        "FR": {"name": "France", "currency": "EUR", "symbol": "€", "locale": "fr-FR", "eu": True},
        "GB": {"name": "United Kingdom", "currency": "GBP", "symbol": "£", "locale": "en-GB", "eu": False},
        "JP": {"name": "Japan", "currency": "JPY", "symbol": "¥", "locale": "ja-JP", "eu": False},
        "KR": {"name": "South Korea", "currency": "KRW", "symbol": "₩", "locale": "ko-KR", "eu": False},
        "IN": {"name": "India", "currency": "INR", "symbol": "₹", "locale": "en-IN", "eu": False},
        "BR": {"name": "Brazil", "currency": "BRL", "symbol": "R$", "locale": "pt-BR", "eu": False},
        "RU": {"name": "Russia", "currency": "RUB", "symbol": "₽", "locale": "ru-RU", "eu": False},
        "AU": {"name": "Australia", "currency": "AUD", "symbol": "A$", "locale": "en-AU", "eu": False},
        "CA": {"name": "Canada", "currency": "CAD", "symbol": "C$", "locale": "en-CA", "eu": False},
        "MX": {"name": "Mexico", "currency": "MXN", "symbol": "MX$", "locale": "es-MX", "eu": False},
        "IT": {"name": "Italy", "currency": "EUR", "symbol": "€", "locale": "it-IT", "eu": True},
        "ES": {"name": "Spain", "currency": "EUR", "symbol": "€", "locale": "es-ES", "eu": True},
        "NL": {"name": "Netherlands", "currency": "EUR", "symbol": "€", "locale": "nl-NL", "eu": True},
        "PL": {"name": "Poland", "currency": "EUR", "symbol": "€", "locale": "pl-PL", "eu": True},
        "SE": {"name": "Sweden", "currency": "SEK", "symbol": "kr", "locale": "sv-SE", "eu": True},
        "CH": {"name": "Switzerland", "currency": "CHF", "symbol": "CHF", "locale": "de-CH", "eu": False},
        "TW": {"name": "Taiwan", "currency": "TWD", "symbol": "NT$", "locale": "zh-TW", "eu": False},
        "HK": {"name": "Hong Kong", "currency": "HKD", "symbol": "HK$", "locale": "zh-HK", "eu": False},
        "SG": {"name": "Singapore", "currency": "SGD", "symbol": "S$", "locale": "en-SG", "eu": False},
        "AE": {"name": "UAE", "currency": "AED", "symbol": "AED", "locale": "ar-AE", "eu": False},
        "SA": {"name": "Saudi Arabia", "currency": "SAR", "symbol": "SAR", "locale": "ar-SA", "eu": False},
        "NL": {"name": "Netherlands", "currency": "EUR", "symbol": "€", "locale": "nl-NL", "eu": True},
        "BE": {"name": "Belgium", "currency": "EUR", "symbol": "€", "locale": "nl-BE", "eu": True},
        "AT": {"name": "Austria", "currency": "EUR", "symbol": "€", "locale": "de-AT", "eu": True},
        "IE": {"name": "Ireland", "currency": "EUR", "symbol": "€", "locale": "en-IE", "eu": True},
        "NZ": {"name": "New Zealand", "currency": "NZD", "symbol": "NZ$", "locale": "en-NZ", "eu": False},
    }

    @classmethod
    def lookup(cls, ip: str, use_free_api: bool = True) -> GeoLocation:
        """
        解析IP对应的地理位置
        
        优先级：
        1. 免费API：ip-api.com (有速率限制)
        2. 内置数据库（降级）
        """
        geo = GeoLocation(ip_address=ip)

        if use_free_api:
            try:
                import urllib.request
                url = f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,region,regionName,city,lat,lon,currency,timezone"
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=3) as resp:
                    data = json.loads(resp.read().decode())
                    if data.get("status") == "success":
                        geo.country_code = data.get("countryCode", "")
                        geo.country_name = data.get("country", "")
                        geo.region = data.get("regionName", "")
                        geo.city = data.get("city", "")
                        geo.city_lat = data.get("lat", 0.0)
                        geo.city_lng = data.get("lon", 0.0)
                        geo.timezone = data.get("timezone", "UTC")
                        country_data = cls.COUNTRY_DATA.get(geo.country_code, {})
                        geo.currency = country_data.get("currency", "USD")
                        geo.currency_symbol = country_data.get("symbol", "$")
                        geo.locale = country_data.get("locale", "en-US")
                        geo.is_eu = country_data.get("eu", False)
                        return geo
            except Exception:
                pass

        # 降级：使用内置数据（如果能匹配到IP段）
        return cls._fallback_lookup(ip)

    @classmethod
    def _fallback_lookup(cls, ip: str) -> GeoLocation:
        """基于IP段模拟解析（开发/测试用）"""
        geo = GeoLocation(ip_address=ip)

        # 简化模拟：如果IP以特定开头，映射到对应国家
        # 真实生产环境应使用MaxMind GeoLite2数据库
        if ip.startswith(("10.", "172.16.", "172.17.", "172.18.", "172.19.",
                          "172.20.", "172.21.", "172.22.", "172.23.", "172.24.",
                          "172.25.", "172.26.", "172.27.", "172.28.", "172.29.",
                          "172.30.", "172.31.", "192.168.")):
            geo.country_code = "US"
            geo.country_name = "United States (Private)"
            geo.currency = "USD"
            geo.currency_symbol = "$"
            geo.locale = "en-US"
            geo.is_eu = False
        else:
            # 默认美国
            geo.country_code = "US"
            geo.country_name = "United States"
            geo.currency = "USD"
            geo.currency_symbol = "$"
            geo.locale = "en-US"
            geo.is_eu = False

        return geo

# ============ 货币换算 ============

class CurrencyConverter:
    """简化汇率转换器"""

    # 基准：USD -> 其他货币（应每日从API更新）
    RATES = {
        "USD": 1.0,
        "EUR": 0.92,
        "GBP": 0.79,
        "CNY": 7.25,
        "JPY": 149.5,
        "KRW": 1320.0,
        "INR": 83.1,
        "BRL": 4.97,
        "RUB": 92.5,
        "AUD": 1.53,
        "CAD": 1.36,
        "MXN": 17.15,
        "CHF": 0.88,
        "TWD": 31.5,
        "HKD": 7.82,
        "SGD": 1.34,
        "AED": 3.67,
        "SAR": 3.75,
        "SEK": 10.45,
        "NZD": 1.64,
        "PLN": 3.98,
    }

    @classmethod
    def convert(cls, amount: float, from_currency: str, to_currency: str) -> float:
        """汇率转换"""
        if from_currency == to_currency:
            return amount
        usd_amount = amount / cls.RATES.get(from_currency, 1.0)
        return round(usd_amount * cls.RATES.get(to_currency, 1.0), 2)

    @classmethod
    def format(cls, amount: float, currency: str) -> str:
        """格式化货币显示"""
        symbols = {
            "USD": "$", "EUR": "€", "GBP": "£", "CNY": "¥",
            "JPY": "¥", "KRW": "₩", "INR": "₹", "BRL": "R$",
            "RUB": "₽", "AUD": "A$", "CAD": "C$", "MXN": "MX$",
            "CHF": "CHF", "TWD": "NT$", "HKD": "HK$", "SGD": "S$",
            "AED": "AED", "SAR": "SAR", "SEK": "kr", "NZD": "NZ$",
            "PLN": "zł",
        }
        symbol = symbols.get(currency, currency + " ")

        # 特殊处理
        if currency in ("JPY", "KRW"):
            return f"{symbol}{int(amount)}"
        return f"{symbol}{amount:,.2f}"

# ============ GEO Targeting Engine ============

class GeoTargeting:
    """
    GEO动态内容引擎

    功能：
    1. IP -> 地理位置解析
    2. 根据地理位置选择内容变体
    3. 货币自动转换 + 显示
    4. 生成GEO个性化HTML/JS片段
    5. 支持GDPR Cookie Consent集成
    """

    def __init__(self, site_url: str = ""):
        self.site_url = site_url
        self.geo_variants: Dict[str, GeoVariant] = {}  # variant_id -> variant
        self.default_variant_id: str = "us"
        self.campaigns: Dict[str, CampaignConfig] = {}

    def add_variant(self, variant: GeoVariant):
        """注册地理内容变体"""
        self.geo_variants[variant.variant_id] = variant
        if variant.is_default:
            self.default_variant_id = variant.variant_id

    def resolve_variant(self, geo: GeoLocation) -> GeoVariant:
        """根据地理位置解析应显示的变体"""
        candidates = []

        for vid, variant in self.geo_variants.items():
            score = 0

            # 排除检查
            if geo.country_code in variant.exclude_countries:
                continue

            # 国家匹配
            if variant.countries and geo.country_code in variant.countries:
                score += 10

            # 货币匹配
            if variant.currencies and geo.currency in variant.currencies:
                score += 5

            # 地区匹配
            if variant.regions and geo.region in variant.regions:
                score += 3

            # 默认变体最低分
            if variant.is_default:
                score = max(score, 0.1)

            if score > 0:
                candidates.append((score, variant))

        if not candidates:
            return self.geo_variants.get(self.default_variant_id,
                list(self.geo_variants.values())[0] if self.geo_variants else GeoVariant(variant_id="default", name="Default"))

        # 返回得分最高的变体
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]

    def detect_geo_from_request(self, request_headers: Dict[str, str], client_ip: str = "") -> GeoLocation:
        """从HTTP请求中检测地理位置"""
        # 优先从X-Forwarded-For获取真实IP
        ip = client_ip
        if not ip and "X-Forwarded-For" in request_headers:
            ip = request_headers["X-Forwarded-For"].split(",")[0].strip()
        if not ip:
            ip = request_headers.get("X-Real-IP", "8.8.8.8")

        return IPLookup.lookup(ip)

    # ===== HTML/JS生成 =====

    def generate_inline_script(self, geo: GeoLocation, variant: GeoVariant) -> str:
        """
        生成内联GEO脚本（<script>内使用）
        将此脚本放在<head>中，可以在页面加载前完成本地化
        """
        data = {
            "geo": {
                "country": geo.country_code,
                "countryName": geo.country_name,
                "city": geo.city,
                "currency": geo.currency,
                "locale": geo.locale,
                "isEU": geo.is_eu,
            },
            "variant": {
                "id": variant.variant_id,
                "name": variant.name,
                "headline": variant.headline,
                "subheadline": variant.subheadline,
                "ctaText": variant.cta_text,
                "ctaUrl": variant.cta_url,
                "priceDisplay": variant.price_display,
                "badge": variant.badge,
                "urgencyMsg": variant.urgency_msg,
            },
            "timestamp": datetime.utcnow().isoformat(),
        }
        return f"window.__GEO_DATA__ = {json.dumps(data, ensure_ascii=False)};"

    def generate_divi_geo_block(self, variant: GeoVariant) -> str:
        """生成Divi/Gutenberg GEO块HTML"""
        blocks = []

        if variant.headline:
            blocks.append(f'<div class="geo-headline" data-geo-only="true">{variant.headline}</div>')
        if variant.badge:
            blocks.append(f'<div class="geo-badge">{variant.badge}</div>')
        if variant.local_price > 0:
            blocks.append(f'<div class="geo-price">{variant.price_display}</div>')
        if variant.urgency_msg:
            blocks.append(f'<div class="geo-urgency">{variant.urgency_msg}</div>')

        return '\n'.join(blocks)

    def generate_js_replacement_script(self, geo: GeoLocation, variant: GeoVariant) -> str:
        """
        生成DOM替换脚本
        在页面加载后，将[data-geo]属性的元素替换为本地化内容
        """
        replacements = {
            "[data-geo='headline']": variant.headline,
            "[data-geo='subheadline']": variant.subheadline,
            "[data-geo='cta-text']": variant.cta_text,
            "[data-geo='badge']": variant.badge,
            "[data-geo='urgency']": variant.urgency_msg,
        }
        currency_symbol = variant.price_display if variant.price_display else geo.currency_symbol
        replacements["[data-geo='price']"] = currency_symbol

        script_lines = [
            "(function() {",
            "  var geo = window.__GEO_DATA__;",
            "  if (!geo) return;",
        ]
        for selector, content in replacements.items():
            escaped_content = content.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")
            selector_escaped = selector.replace("'", "\\'")
            script_lines.append(
                f"  var el = document.querySelector('{selector_escaped}');"
                f"  if (el) el.textContent = '{escaped_content}';"
            )
        script_lines.append("})();")

        return "\n".join(script_lines)

    # ===== 大促页面自动切换 =====

    def add_campaign(self, campaign: CampaignConfig):
        """注册大促配置"""
        self.campaigns[campaign.name] = campaign

    def get_active_campaign(self, geo: GeoLocation) -> Optional[Tuple[CampaignConfig, GeoVariant]]:
        """获取当前活跃的大促（如果地理位置匹配）"""
        now = datetime.utcnow()
        for name, campaign in self.campaigns.items():
            if not campaign.active:
                continue
            if campaign.start_time <= now <= campaign.end_time:
                # 找匹配的变体
                for variant in campaign.variants:
                    if variant.countries and geo.country_code not in variant.countries:
                        continue
                    return campaign, variant
                # 使用默认变体
                default = next((v for v in campaign.variants if v.variant_id == campaign.default_variant), None)
                if default:
                    return campaign, default
        return None

    def generate_campaign_banner(self, campaign: CampaignConfig, variant: GeoVariant, geo: GeoLocation) -> str:
        """生成大促横幅HTML"""
        badge_emoji = {
            "CN": "🇨🇳", "DE": "🇩🇪", "FR": "🇫🇷", "GB": "🇬🇧",
            "JP": "🇯🇵", "KR": "🇰🇷", "IN": "🇮🇳", "BR": "🇧🇷",
            "AU": "🇦🇺", "CA": "🇨🇦", "MX": "🇲🇽", "IT": "🇮🇹",
            "ES": "🇪🇸", "NL": "🇳🇱", "SG": "🇸🇬", "US": "🇺🇸",
        }
        emoji = badge_emoji.get(geo.country_code, "🌍")
        price_display = variant.price_display or f"{geo.currency_symbol}{campaign.name.split('_')[0]}"

        return f"""
<div class="campaign-banner" data-campaign="{campaign.name}" style="
    background: linear-gradient(135deg, #e94560, #0f3460);
    color: white;
    padding: 0.75rem 1.5rem;
    text-align: center;
    font-size: 0.95rem;
    font-weight: 600;
    position: relative;
">
    <span class="campaign-badge">{emoji} {variant.badge}</span>
    <span class="campaign-msg">{variant.urgency_msg}</span>
    <span class="campaign-price" style="margin-left:1rem;background:#fff;color:#e94560;padding:0.2rem 0.6rem;border-radius:20px;font-size:0.85rem;">
        {price_display}
    </span>
</div>"""

    # ===== WordPress mu-plugin 生成 =====

    def generate_wp_mu_plugin(self) -> str:
        """生成WordPress mu-plugin代码（自动GEO重定向/内容替换）"""
        geo_json_snippet = json.dumps({
            vid: {
                "countries": v.countries,
                "headline": v.headline,
                "badge": v.badge,
                "priceDisplay": v.price_display,
                "ctaText": v.cta_text,
            }
            for vid, v in self.geo_variants.items()
        }, ensure_ascii=False)

        geo_json_escaped = geo_json_snippet.replace("{", "{{").replace("}", "}}")
        php_code = """<?php
/**
 * Auto-Claw GEO Targeting Plugin
 * Generated: """ + datetime.utcnow().isoformat() + """
 */

add_action('wp_head', 'auto_claw_geo_inline_script', 1);
add_action('wp_footer', 'auto_claw_geo_replacement', 99);

function auto_claw_geo_get_visitor_country() {
    // 优先从Cloudflare/Varnish获取真实国家
    $headers_to_check = [
        'HTTP_CF_IPCOUNTRY',      // Cloudflare
        'X-VCOS-Geolocation',     // Varnish
        'X-Geo-IP-Country',       // Nginx geo module
        'GEOIP_COUNTRY_CODE',     // Apache mod_geoip
    ];
    foreach ($headers_to_check as $header) {
        if (isset($_SERVER[$header]) && !empty($_SERVER[$header])) {
            return strtoupper($_SERVER[$header]);
        }
    }
    return 'US'; // 默认美国
}

function auto_claw_geo_inline_script() {
    $country = auto_claw_geo_get_visitor_country();
    $geo_variants = """ + geo_json_snippet + """;
    $matched = 'us';

    foreach ($geo_variants as $vid => $v) {
        if (!empty($v['countries']) && in_array($country, $v['countries'])) {
            $matched = $vid;
            break;
        }
    }
    $v = $geo_variants[$matched] ?? ($geo_variants['us'] ?? []);

    $geo_data = json_encode([
        'country' => $country,
        'variant' => $matched,
        'headline' => $v['headline'] ?? '',
        'badge' => $v['badge'] ?? '',
        'priceDisplay' => $v['priceDisplay'] ?? '',
        'ctaText' => $v['ctaText'] ?? '',
    ]);
    echo "<script>window.__GEO_DATA__ = $geo_data;</script>";
}

function auto_claw_geo_replacement() {
    echo '<script>
    (function() {
        var geo = window.__GEO_DATA__;
        if (!geo || !geo.variant) return;
        document.querySelectorAll("[data-geo]").forEach(function(el) {
            var key = el.getAttribute("data-geo");
            if (geo.variant && geo.variant[key]) {
                el.textContent = geo.variant[key];
            }
        });
    })();
    </script>';
}
"""
        return php_code


# ============ 智能落地页生成器 ============

class SmartLandingPage:
    """
    基于GEO的智能落地页生成器
    根据访客地理位置自动生成个性化落地页URL
    """

    def __init__(self, geo_targeting: GeoTargeting):
        self.geo = geo_targeting
        self.base_slug = "/landing"
        self.country_slugs: Dict[str, str] = {}  # country_code -> slug

    def register_country_slug(self, country_code: str, slug: str):
        """注册国家对应的落地页slug"""
        self.country_slugs[country_code] = slug

    def get_landing_url(self, geo: GeoLocation, base_url: str = "") -> str:
        """获取最适合该用户的落地页URL"""
        slug = self.country_slugs.get(geo.country_code, self.base_slug)
        url = f"{base_url.rstrip('/')}{slug}"

        # 添加UTM参数追踪
        separator = "?" if "?" not in url else "&"
        url = f"{url}{separator}geo={geo.country_code}&curr={geo.currency}&locale={geo.locale}"

        return url

    def generate_landing_page_content(self, geo: GeoLocation, variant: GeoVariant) -> str:
        """生成完整的落地页HTML"""
        badge_emoji = {
            "CN": "🇨🇳 中文支持", "DE": "🇩🇪 Schnelle Lieferung", "FR": "🇫🇷 Livraison rapide",
            "GB": "🇬🇧 Free UK Delivery", "JP": "🇯🇵 日本語サポート", "KR": "🇰🇷 한국어 지원",
            "IN": "🇮🇳 Free Shipping", "AU": "🇦🇺 Fast Delivery", "US": "🇺🇸 Free Shipping",
        }
        badge = badge_emoji.get(geo.country_code, "🌍 International")

        html = f"""<!DOCTYPE html>
<html lang="{geo.locale.split('-')[0]}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{variant.headline or "Welcome"} - {geo.country_name}</title>
    <meta name="description" content="{variant.subheadline or 'Personalized for you'}">
    <script>window.__GEO_DATA__ = {{
        "country": "{geo.country_code}",
        "countryName": "{geo.country_name}",
        "currency": "{geo.currency}",
        "locale": "{geo.locale}",
        "variant": "{variant.variant_id}"
    }};</script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: system-ui, -apple-system, sans-serif; }}
        .geo-hero {{
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            text-align: center;
            padding: 2rem;
        }}
        .geo-hero .badge {{
            display: inline-block;
            background: rgba(255,255,255,0.15);
            padding: 0.4rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            margin-bottom: 1.5rem;
        }}
        .geo-hero h1 {{
            font-size: clamp(2rem, 5vw, 3.5rem);
            margin-bottom: 1rem;
            line-height: 1.2;
        }}
        .geo-hero .subheadline {{
            font-size: 1.2rem;
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto 2rem;
        }}
        .geo-cta {{
            display: inline-block;
            background: #e94560;
            color: white;
            padding: 1rem 2.5rem;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 700;
            text-decoration: none;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .geo-cta:hover {{ transform: translateY(-2px); box-shadow: 0 8px 25px rgba(233,69,96,0.4); }}
        .geo-price {{
            margin-top: 1.5rem;
            font-size: 2rem;
            font-weight: 700;
        }}
        .geo-price .currency {{ font-size: 1.2rem; opacity: 0.8; }}
        .geo-urgency {{
            margin-top: 1rem;
            font-size: 0.9rem;
            color: #ffcc00;
        }}
    </style>
</head>
<body>
    <section class="geo-hero">
        <div>
            <div class="badge" data-geo="badge">{variant.badge or badge}</div>
            <h1 data-geo="headline">{variant.headline}</h1>
            <p class="subheadline" data-geo="subheadline">{variant.subheadline}</p>
            <a href="{variant.cta_url}" class="geo-cta" data-geo="cta-text">{variant.cta_text or "Get Started"}</a>
            <div class="geo-price" data-geo="price">{variant.price_display or f"{geo.currency_symbol}99"}</div>
            <div class="geo-urgency" data-geo="urgency">{variant.urgency_msg}</div>
        </div>
    </section>
    <script src="/wp-content/mu-plugins/auto-claw-geo.js"></script>
</body>
</html>"""
        return html


# ============ Demo ============

def demo():
    """演示"""
    geo = GeoTargeting("https://example.com")

    # 注册变体
    geo.add_variant(GeoVariant(
        variant_id="us", name="美国",
        countries=["US", "CA", "MX"],
        headline="Your 24/7 AI Workforce",
        subheadline="Automate your business operations with AI",
        cta_text="Start Free Trial", cta_url="/signup",
        price_display="$99/mo", badge="🇺🇸 Free US Shipping",
        urgency_msg="Limited: 30% off ends tonight!",
        is_default=True
    ))
    geo.add_variant(GeoVariant(
        variant_id="eu", name="欧盟",
        countries=["DE", "FR", "IT", "ES", "NL", "PL", "BE", "AT", "IE", "SE"],
        headline="Ihr KI-gestützter 24/7 Mitarbeiter",
        subheadline="Automatisieren Sie Ihre Geschäftsprozesse mit KI",
        cta_text="Kostenlos testen", cta_url="/de/signup",
        price_display="€89/mo", badge="🇩🇪 Kostenloser Versand",
        urgency_msg="Angebot: 30% Rabatt heute!",
    ))
    geo.add_variant(GeoVariant(
        variant_id="cn", name="中国",
        countries=["CN", "TW", "HK"],
        headline="您的24/7 AI智能助手",
        subheadline="用AI自动化您的业务流程",
        cta_text="免费试用", cta_url="/zh/signup",
        price_display="¥699/月", badge="🇨🇳 中文支持",
        urgency_msg="限时优惠：今日7折！",
    ))

    # 模拟来自德国的访客
    test_ip = "85.214.132.117"  # 德国柏林示例IP
    geo_loc = IPLookup.lookup(test_ip, use_free_api=False)
    print(f"IP: {test_ip}")
    print(f"位置: {geo_loc.country_name} ({geo_loc.country_code})")
    print(f"货币: {geo_loc.currency} {geo_loc.currency_symbol}")
    print(f"语言: {geo_loc.locale}")
    print(f"欧盟: {geo_loc.is_eu}")

    variant = geo.resolve_variant(geo_loc)
    print(f"\n匹配变体: {variant.name} ({variant.variant_id})")
    print(f"  标题: {variant.headline}")
    print(f"  CTA: {variant.cta_text}")
    print(f"  价格: {variant.price_display}")

    # 货币转换演示
    base_price_usd = 99
    for currency in ["USD", "EUR", "GBP", "CNY", "JPY"]:
        converted = CurrencyConverter.convert(base_price_usd, "USD", currency)
        formatted = CurrencyConverter.format(converted, currency)
        print(f"  {currency}: {formatted}")

    # 动态落地页演示
    landing = SmartLandingPage(geo)
    landing.register_country_slug("US", "/landing/us")
    landing.register_country_slug("DE", "/landing/eu")
    landing.register_country_slug("CN", "/landing/cn")

    landing_url = landing.get_landing_url(geo_loc, "https://example.com")
    print(f"\n个性化落地页: {landing_url}")


if __name__ == "__main__":
    demo()

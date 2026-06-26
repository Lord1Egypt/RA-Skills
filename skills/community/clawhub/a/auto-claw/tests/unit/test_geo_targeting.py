"""
Unit tests for src/geo_targeting.py — GEO Dynamic Content Engine
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import geo_targeting as geo


class TestIPLookup:
    """Test IP to geo location lookup."""

    def test_lookup_returns_geo_location(self):
        """IP lookup returns GeoLocation for known IP."""
        result = geo.IPLookup.lookup("8.8.8.8")
        assert isinstance(result, geo.GeoLocation)

    def test_country_code_extracted(self):
        """Country code is extracted from IP."""
        result = geo.IPLookup.lookup("8.8.8.8")
        assert result.country_code is not None
        assert len(result.country_code) == 2


class TestCurrencyConverter:
    """Test multi-currency conversion."""

    def test_convert_returns_number(self):
        """convert() returns numeric result."""
        result = geo.CurrencyConverter.convert(100, "USD", "EUR")
        assert isinstance(result, (int, float))
        assert result > 0

    def test_same_currency_returns_same(self):
        """USD to USD = same amount."""
        result = geo.CurrencyConverter.convert(99, "USD", "USD")
        assert result == 99

    def test_format_produces_string(self):
        """format() produces formatted price string."""
        result = geo.CurrencyConverter.format(99.99, "USD")
        assert isinstance(result, str)
        assert "99" in result


class TestGeoTargetingModule:
    """Smoke tests for GeoTargeting engine."""

    def test_geotargeting_class_exists(self):
        """GeoTargeting class exists."""
        assert hasattr(geo, 'GeoTargeting')

    def test_campaignconfig_class_exists(self):
        """CampaignConfig class exists."""
        assert hasattr(geo, 'CampaignConfig')

    def test_smart_landing_page_exists(self):
        """SmartLandingPage class exists."""
        assert hasattr(geo, 'SmartLandingPage')

    def test_generate_wp_mu_plugin_returns_string(self):
        """generate_wp_mu_plugin() returns string."""
        gt = geo.GeoTargeting()
        code = gt.generate_wp_mu_plugin()
        assert isinstance(code, str)
        assert len(code) > 50

    def test_inline_script_with_real_objects(self):
        """generate_inline_script() works with real GeoLocation and GeoVariant."""
        gt = geo.GeoTargeting()
        location = geo.IPLookup.lookup("8.8.8.8")
        variant = geo.GeoVariant(
            variant_id="us_variant",
            name="US Variant",
            headline="Test",
            cta_text="Click",
        )
        script = gt.generate_inline_script(location, variant)
        assert isinstance(script, str)

    def test_campaign_banner_with_real_objects(self):
        """generate_campaign_banner() works with real CampaignConfig, GeoVariant, GeoLocation."""
        gt = geo.GeoTargeting()
        location = geo.IPLookup.lookup("8.8.8.8")
        variant = geo.GeoVariant(
            variant_id="us_variant",
            name="US Variant",
            headline="Test",
            cta_text="Click",
        )
        import datetime
        campaign = geo.CampaignConfig(
            name="black_friday",
            start_time=datetime.datetime(2026, 11, 27),
            end_time=datetime.datetime(2026, 11, 30),
        )
        banner = gt.generate_campaign_banner(campaign, variant, location)
        assert isinstance(banner, str)

    def test_geolocation_dataclass(self):
        """GeoLocation dataclass has expected fields."""
        gl = geo.GeoLocation(
            ip_address="8.8.8.8",
            country_code="US",
            country_name="United States",
            city="Mountain View",
            region="California",
            locale="en-US",
            currency="USD",
            timezone="America/Los_Angeles",
        )
        assert gl.country_code == "US"
        assert gl.currency == "USD"

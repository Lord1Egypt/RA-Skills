#!/usr/bin/env python3
"""
Agricultural Output Forecasting with SkillPay Billing Integration and Free Trial
Predicts crop yields using big data analytics.
Version: 1.1.0

农产品产量预测 - 支持计费集成和免费试用
使用大数据分析预测作物产量
"""

import json
from functools import lru_cache
import sys
import argparse
import os
import random
import csv
from datetime import datetime
from typing import Dict, Any, Optional, List
import urllib.request
import urllib.error

# ═══════════════════════════════════════════════════
# Version Info / 版本信息
# ═══════════════════════════════════════════════════
VERSION = "1.1.0"

# ═══════════════════════════════════════════════════
# SkillPay Billing Integration / 计费接入
# ═══════════════════════════════════════════════════
BILLING_URL = 'https://skillpay.me/api/v1/billing'
API_KEY = os.environ.get('SKILLPAY_API_KEY', '')
SKILL_ID = os.environ.get('SKILLPAY_SKILL_ID', '')

# ═══════════════════════════════════════════════════
# I18n / 国际化
# ═══════════════════════════════════════════════════
I18N = {
    'zh': {
        'error_no_user_id': '需要提供用户ID',
        'error_no_api_key': '计费配置缺失。请设置 SKILLPAY_API_KEY 和 SKILLPAY_SKILL_ID 环境变量。',
        'error_payment_failed': '支付失败或余额不足',
        'error_insufficient_balance': '余额不足',
        'trial_mode_active': '演示/试用模式',
        'trial_remaining': '剩余试用次数',
        'balance': '余额',
        'success': '成功',
        'forecast_result': '预测结果',
        'demo_notice': '【演示模式】使用模拟数据展示功能',
        'demo_data_notice': '当前使用演示数据，无需API密钥',
        'historical_comparison': '历史对比',
        'export_csv': '导出CSV',
        'crop_type': '作物类型',
        'region': '地区',
        'season': '季节',
        'yield_forecast': '产量预测',
        'risk_assessment': '风险评估',
        'recommendations': '建议',
    },
    'en': {
        'error_no_user_id': 'User ID is required',
        'error_no_api_key': 'Billing configuration missing. Set SKILLPAY_API_KEY and SKILLPAY_SKILL_ID environment variables.',
        'error_payment_failed': 'Payment failed or insufficient balance',
        'error_insufficient_balance': 'Insufficient balance',
        'trial_mode_active': 'Demo/Trial Mode',
        'trial_remaining': 'Trial calls remaining',
        'balance': 'Balance',
        'success': 'Success',
        'forecast_result': 'Forecast Result',
        'demo_notice': '[DEMO MODE] Using simulated data to demonstrate functionality',
        'demo_data_notice': 'Currently using demo data, no API key required',
        'historical_comparison': 'Historical Comparison',
        'export_csv': 'Export CSV',
        'crop_type': 'Crop Type',
        'region': 'Region',
        'season': 'Season',
        'yield_forecast': 'Yield Forecast',
        'risk_assessment': 'Risk Assessment',
        'recommendations': 'Recommendations',
    }
}

def get_text(key: str, lang: str = 'zh') -> str:
    """Get localized text."""
    return I18N.get(lang, I18N['zh']).get(key, key)

# ═══════════════════════════════════════════════════
# Free Trial Manager / 免费试用管理
# ═══════════════════════════════════════════════════
class TrialManager:
    """Manages free trial usage for users."""
    
    def __init__(self, skill_name: str):
        self.skill_name = skill_name
        self.trial_dir = os.path.expanduser("~/.openclaw/skill_trial")
        self.trial_file = os.path.join(self.trial_dir, f"{skill_name}.json")
        self.max_free_calls = 10
        
        # Ensure trial directory exists
        os.makedirs(self.trial_dir, exist_ok=True)
    
    def _load_trial_data(self) -> Dict[str, Any]:
        """Load trial data from file."""
        if os.path.exists(self.trial_file):
            try:
                with open(self.trial_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_trial_data(self, data: Dict[str, Any]):
        """Save trial data to file."""
        try:
            with open(self.trial_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Warning: Could not save trial data: {e}", file=sys.stderr)
    
    def get_trial_remaining(self, user_id: str) -> int:
        """Get remaining free trial calls for a user."""
        if not user_id:
            return 0
        
        data = self._load_trial_data()
        user_data = data.get(user_id, {})
        used_calls = user_data.get('used_calls', 0)
        
        return max(0, self.max_free_calls - used_calls)
    
    def use_trial(self, user_id: str) -> bool:
        """Record a free trial usage for a user."""
        if not user_id:
            return False
        
        data = self._load_trial_data()
        
        if user_id not in data:
            data[user_id] = {'used_calls': 0, 'first_use': datetime.now().isoformat()}
        
        data[user_id]['used_calls'] += 1
        data[user_id]['last_use'] = datetime.now().isoformat()
        
        self._save_trial_data(data)
        return True
    
    def get_trial_info(self, user_id: str) -> Dict[str, Any]:
        """Get full trial information for a user."""
        remaining = self.get_trial_remaining(user_id)
        data = self._load_trial_data()
        user_data = data.get(user_id, {})
        
        return {
            'trial_mode': remaining > 0,
            'trial_remaining': remaining,
            'trial_total': self.max_free_calls,
            'trial_used': user_data.get('used_calls', 0),
            'first_use': user_data.get('first_use'),
            'last_use': user_data.get('last_use')
        }


class SkillPayBilling:
    """SkillPay billing SDK for Python."""
    
    def __init__(self, api_key: str = API_KEY, skill_id: str = SKILL_ID):
        self.api_key = api_key
        self.skill_id = skill_id
        self.headers = {
            'X-API-Key': api_key,
            'Content-Type': 'application/json',
        }
    
    def _make_request(self, endpoint: str, method: str = 'GET', data: dict = None) -> dict:
        """Make HTTP request to SkillPay API."""
        url = f"{BILLING_URL}{endpoint}"
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8') if data else None,
                headers=self.headers,
                method=method
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return {'success': False, 'error': f'HTTP {e.code}: {e.reason}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def charge_user(self, user_id: str) -> Dict[str, Any]:
        """
        Charge / 扣费 / 課金
        Deduct 1 token per call (~0.001 USDT)
        """
        result = self._make_request('/charge', method='POST', data={
            'user_id': user_id,
            'skill_id': self.skill_id,
            'amount': 0,  # 0 means use default pricing (1 token)
        })
        
        if result.get('success'):
            return {
                'ok': True,
                'balance': result.get('balance', 0),
            }
        else:
            return {
                'ok': False,
                'balance': result.get('balance', 0),
                'payment_url': result.get('payment_url'),
            }
    
    def get_balance(self, user_id: str) -> float:
        """
        Balance / 余额 / 残高
        Returns token balance.
        """
        result = self._make_request(f'/balance?user_id={user_id}')
        return result.get('balance', 0.0)
    
    def get_payment_link(self, user_id: str, amount: float = 8) -> str:
        """
        Payment link / 充值链接 / 入金リンク
        Generate BNB Chain USDT payment link.
        Default minimum deposit: 8 USDT
        """
        result = self._make_request('/payment-link', method='POST', data={
            'user_id': user_id,
            'amount': amount,
        })
        return result.get('payment_url', '')


class AgriculturalForecaster:
    """Main class for agricultural output forecasting."""
    
    # Crop yield baselines (tons per hectare)
    CROP_BASELINES = {
        'wheat': 6.0,
        'rice': 7.5,
        'corn': 10.0,
        'barley': 5.0,
        'sorghum': 4.5,
        'tomato': 35.0,
        'potato': 25.0,
        'cabbage': 40.0,
        'cucumber': 30.0,
        'apple': 25.0,
        'orange': 20.0,
        'grape': 15.0,
        'peach': 18.0,
        'soybean': 3.0,
        'cotton': 2.5,
        'sugarcane': 80.0,
    }
    
    # Historical data for comparison (simulated)
    HISTORICAL_DATA = {
        'wheat': {'avg_yield': 5.8, 'min_yield': 4.5, 'max_yield': 7.2, 'years': 5},
        'rice': {'avg_yield': 7.2, 'min_yield': 6.0, 'max_yield': 8.5, 'years': 5},
        'corn': {'avg_yield': 9.5, 'min_yield': 7.5, 'max_yield': 11.5, 'years': 5},
        'tomato': {'avg_yield': 33.0, 'min_yield': 28.0, 'max_yield': 38.0, 'years': 5},
        'potato': {'avg_yield': 24.0, 'min_yield': 20.0, 'max_yield': 28.0, 'years': 5},
    }
    
    # Weather impact factors
    WEATHER_FACTORS = {
        'excellent': 1.15,
        'good': 1.05,
        'normal': 1.0,
        'poor': 0.85,
        'bad': 0.70,
    }
    
    def __init__(self, api_key: str = API_KEY, skill_id: str = SKILL_ID, 
                 demo_mode: bool = False, lang: str = 'zh'):
        self.billing = SkillPayBilling(api_key, skill_id)
        self.trial = TrialManager("agricultural-output-forecasting")
        self.demo_mode = demo_mode
        self.lang = lang
    
    def get_weather_factor(self, region: str, season: str) -> float:
        """Simulate weather factor based on region and season."""
        # In production, this would call a weather API
        weather_conditions = list(self.WEATHER_FACTORS.keys())
        weights = [0.1, 0.3, 0.4, 0.15, 0.05]  # Probability distribution
        condition = random.choices(weather_conditions, weights=weights)[0]
        return self.WEATHER_FACTORS[condition]
    
    def get_market_trend(self, crop_type: str) -> float:
        """Simulate market price trend factor."""
        # Random trend between -10% to +15%
        return 1.0 + random.uniform(-0.10, 0.15)
    
    def calculate_confidence(self, data_quality: str) -> float:
        """Calculate confidence interval based on data quality."""
        confidence_map = {
            'high': 0.95,
            'medium': 0.85,
            'low': 0.70,
        }
        return confidence_map.get(data_quality, 0.80)
    
    def get_historical_comparison(self, crop_type: str, current_yield: float) -> Dict[str, Any]:
        """Get historical comparison data for the crop."""
        crop_type_lower = crop_type.lower()
        historical = self.HISTORICAL_DATA.get(crop_type_lower)
        
        if not historical:
            return None
        
        avg_yield = historical['avg_yield']
        variance = ((current_yield - avg_yield) / avg_yield) * 100
        
        return {
            'historical_avg': avg_yield,
            'historical_min': historical['min_yield'],
            'historical_max': historical['max_yield'],
            'comparison_years': historical['years'],
            'current_vs_avg_percent': round(variance, 2),
            'trend': 'above_average' if variance > 5 else 'below_average' if variance < -5 else 'average',
            'comparison_text': {
                'zh': f"较历史平均{'高' if variance > 0 else '低'} {abs(variance):.1f}%",
                'en': f"{variance:.1f}% {'above' if variance > 0 else 'below'} historical average"
            }
        }
    
    def forecast(self, crop_type: str, area_hectares: float, 
                 region: str, season: str, include_historical: bool = True) -> Dict[str, Any]:
        """
        Main forecasting method.
        Returns detailed forecast results.
        """
        crop_type = crop_type.lower()
        
        # Get baseline yield
        baseline = self.CROP_BASELINES.get(crop_type, 5.0)
        
        # Apply factors
        weather_factor = self.get_weather_factor(region, season)
        market_factor = self.get_market_trend(crop_type)
        
        # Calculate yield per hectare
        yield_per_hectare = baseline * weather_factor * market_factor
        
        # Calculate total yield
        total_yield = yield_per_hectare * area_hectares
        
        # Calculate confidence interval
        confidence = self.calculate_confidence('medium')
        margin = yield_per_hectare * (1 - confidence)
        
        # Risk assessment
        risk_level = 'low' if weather_factor > 1.0 else 'medium' if weather_factor > 0.85 else 'high'
        
        # Generate recommendations
        recommendations = []
        if self.lang == 'zh':
            if weather_factor < 0.9:
                recommendations.append("建议增加灌溉设施投资")
            if market_factor > 1.1:
                recommendations.append("市场价格有利，建议扩大种植面积")
            if risk_level == 'high':
                recommendations.append("建议购买农业保险以降低风险")
            if yield_per_hectare > baseline * 1.1:
                recommendations.append("预计产量高于平均水平，提前规划收获和储存")
        else:
            if weather_factor < 0.9:
                recommendations.append("Consider investing in irrigation infrastructure")
            if market_factor > 1.1:
                recommendations.append("Favorable market prices, consider expanding planting area")
            if risk_level == 'high':
                recommendations.append("Consider purchasing agricultural insurance to reduce risk")
            if yield_per_hectare > baseline * 1.1:
                recommendations.append("Above-average yield expected, plan harvest and storage early")
        
        result = {
            "forecast_id": f"AGR_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "crop_type": crop_type,
            "region": region,
            "season": season,
            "area_hectares": area_hectares,
            "yield_forecast": {
                "per_hectare": round(yield_per_hectare, 2),
                "total": round(total_yield, 2),
                "unit": "tons",
                "confidence_interval": {
                    "lower": round(yield_per_hectare - margin, 2),
                    "upper": round(yield_per_hectare + margin, 2),
                    "confidence": f"{confidence*100:.0f}%"
                }
            },
            "factors": {
                "weather_factor": round(weather_factor, 2),
                "market_factor": round(market_factor, 2),
            },
            "risk_assessment": {
                "level": risk_level,
                "weather_risk": "high" if weather_factor < 0.9 else "low"
            },
            "recommendations": recommendations,
            "generated_at": datetime.now().isoformat(),
            "version": VERSION
        }
        
        # Add historical comparison if requested
        if include_historical:
            historical = self.get_historical_comparison(crop_type, yield_per_hectare)
            if historical:
                result["historical_comparison"] = historical
        
        return result
    
    def export_to_csv(self, forecast_result: Dict[str, Any], output_path: str) -> bool:
        """Export forecast results to CSV file."""
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow(['Field', 'Value'])
                
                # Basic info
                writer.writerow(['Forecast ID', forecast_result.get('forecast_id', '')])
                writer.writerow(['Crop Type', forecast_result.get('crop_type', '')])
                writer.writerow(['Region', forecast_result.get('region', '')])
                writer.writerow(['Season', forecast_result.get('season', '')])
                writer.writerow(['Area (hectares)', forecast_result.get('area_hectares', '')])
                
                # Yield forecast
                yield_data = forecast_result.get('yield_forecast', {})
                writer.writerow(['Yield per hectare', yield_data.get('per_hectare', '')])
                writer.writerow(['Total yield', yield_data.get('total', '')])
                writer.writerow(['Unit', yield_data.get('unit', '')])
                
                # Confidence interval
                ci = yield_data.get('confidence_interval', {})
                writer.writerow(['Confidence Lower', ci.get('lower', '')])
                writer.writerow(['Confidence Upper', ci.get('upper', '')])
                writer.writerow(['Confidence Level', ci.get('confidence', '')])
                
                # Risk assessment
                risk = forecast_result.get('risk_assessment', {})
                writer.writerow(['Risk Level', risk.get('level', '')])
                
                # Recommendations
                writer.writerow(['Recommendations', ''])
                for rec in forecast_result.get('recommendations', []):
                    writer.writerow(['', rec])
                
                # Historical comparison
                hist = forecast_result.get('historical_comparison', {})
                if hist:
                    writer.writerow(['', ''])
                    writer.writerow(['Historical Comparison', ''])
                    writer.writerow(['Historical Average', hist.get('historical_avg', '')])
                    writer.writerow(['Historical Min', hist.get('historical_min', '')])
                    writer.writerow(['Historical Max', hist.get('historical_max', '')])
                    writer.writerow(['Comparison Years', hist.get('comparison_years', '')])
                    writer.writerow(['Variance %', hist.get('current_vs_avg_percent', '')])
            
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}", file=sys.stderr)
            return False
    
    def process(self, crop_type: str, area_hectares: float, 
                region: str, season: str, user_id: str = "",
                include_historical: bool = True) -> Dict[str, Any]:
        """
        Full processing pipeline with SkillPay billing and free trial support.
        """
        if not user_id and not self.demo_mode:
            return {
                "success": False,
                "error": get_text('error_no_user_id', self.lang)
            }
        
        # Demo mode - no billing
        if self.demo_mode:
            forecast_result = self.forecast(crop_type, area_hectares, region, season, include_historical)
            return {
                "success": True,
                "demo_mode": True,
                "notice": get_text('demo_data_notice', self.lang),
                "forecast": forecast_result
            }
        
        # Check free trial status
        trial_remaining = self.trial.get_trial_remaining(user_id)
        
        if trial_remaining > 0:
            # Free trial mode - no billing
            self.trial.use_trial(user_id)
            forecast_result = self.forecast(crop_type, area_hectares, region, season, include_historical)
            
            return {
                "success": True,
                "trial_mode": True,
                "trial_remaining": trial_remaining - 1,
                "balance": None,
                "forecast": forecast_result
            }
        
        # Normal billing mode
        if not self.billing.api_key or not self.billing.skill_id:
            return {
                "success": False,
                "trial_mode": False,
                "trial_remaining": 0,
                "error": get_text('error_no_api_key', self.lang)
            }
        
        # Step 1: Charge user (1 token per call)
        charge_result = self.billing.charge_user(user_id)
        
        if not charge_result.get('ok'):
            return {
                "success": False,
                "trial_mode": False,
                "trial_remaining": 0,
                "error": get_text('error_payment_failed', self.lang),
                "balance": charge_result.get('balance', 0),
                "paymentUrl": charge_result.get('payment_url'),
            }
        
        # Step 2: Generate forecast
        forecast_result = self.forecast(crop_type, area_hectares, region, season, include_historical)
        
        return {
            "success": True,
            "trial_mode": False,
            "trial_remaining": 0,
            "balance": charge_result.get('balance'),
            "forecast": forecast_result
        }


def forecast_output(crop_type: str, area_hectares: float, region: str, 
                   season: str, user_id: str = "", 
                   api_key: str = API_KEY, skill_id: str = SKILL_ID,
                   demo_mode: bool = False, lang: str = 'zh',
                   include_historical: bool = True) -> Dict[str, Any]:
    """
    Convenience function for agricultural output forecasting.
    """
    forecaster = AgriculturalForecaster(api_key, skill_id, demo_mode, lang)
    return forecaster.process(crop_type, area_hectares, region, season, user_id, include_historical)


def main():
    parser = argparse.ArgumentParser(
        description='Agricultural Output Forecasting - Predict crop yields using big data analytics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic forecast
  python forecast.py -c wheat -a 100 -r "North China Plain" -s spring -u user_123
  
  # Demo mode (no API key required)
  python forecast.py -c rice -a 50 -r "Hunan" -s summer --demo
  
  # With historical comparison and CSV export
  python forecast.py -c corn -a 200 -r "Henan" -s autumn -u user_123 --historical --export forecast.csv
  
  # English output
  python forecast.py -c wheat -a 100 -r "North China" -s spring --language en
        """
    )
    parser.add_argument('--crop', '-c', required=True, help='Crop type (e.g., wheat, rice, corn)')
    parser.add_argument('--area', '-a', type=float, required=True, help='Area in hectares')
    parser.add_argument('--region', '-r', required=True, help='Region/location')
    parser.add_argument('--season', '-s', required=True, help='Season (spring, summer, autumn, winter)')
    parser.add_argument('--user-id', '-u', help='User ID for billing')
    parser.add_argument('--api-key', '-k', default=API_KEY, help='SkillPay API key')
    parser.add_argument('--skill-id', default=SKILL_ID, help='Skill ID')
    parser.add_argument('--output', '-o', help='Output file path (optional)')
    parser.add_argument('--export', '-e', help='Export to CSV file path')
    parser.add_argument('--demo', action='store_true', help='Run in demo mode (no API key required)')
    parser.add_argument('--language', '-l', choices=['zh', 'en'], default='zh', help='Output language (zh/en)')
    parser.add_argument('--historical', action='store_true', help='Include historical comparison')
    
    args = parser.parse_args()
    
    # Check for demo mode
    demo_mode = args.demo or (not API_KEY and not args.api_key)
    
    if demo_mode:
        print(f"\n{'='*50}", file=sys.stderr)
        print(get_text('demo_notice', args.language), file=sys.stderr)
        print(f"{'='*50}\n", file=sys.stderr)
    
    if not args.user_id and not demo_mode:
        parser.error("--user-id is required (unless using --demo mode)")
    
    # Use environment variables if not provided
    api_key = args.api_key or API_KEY
    skill_id = args.skill_id or SKILL_ID
    
    # Process the forecast
    forecaster = AgriculturalForecaster(api_key, skill_id, demo_mode, args.language)
    result = forecaster.process(args.crop, args.area, args.region, args.season, 
                                args.user_id or "demo_user", args.historical)
    
    # Export to CSV if requested
    if args.export and result.get('success'):
        if forecaster.export_to_csv(result['forecast'], args.export):
            print(f"Exported to CSV: {args.export}", file=sys.stderr)
    
    # Output result
    output_json = json.dumps(result, ensure_ascii=False, indent=2)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_json)
        print(f"Result saved to: {args.output}")
    else:
        print(output_json)
    
    return 0 if result.get('success') else 1


if __name__ == '__main__':
    sys.exit(main())

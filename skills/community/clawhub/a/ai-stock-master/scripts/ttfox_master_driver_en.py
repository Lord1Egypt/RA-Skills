try:
    import requests
    DEPENDENCY_OK = True
except ImportError:
    DEPENDENCY_OK = False
    print("[Warning] 'requests' library not found. Please run 'pip install requests' to enable AI analysis.")
import json
import urllib.parse
import traceback

class TTFoxMasterAgentEn:
    """
    TTFox Master Agent - OpenClaw Global API Driver (English Edition)
    Fully aligned with the CN version logic but outputs in professional English.
    """
    
    def __init__(self):
        self.base_url = "https://master.ttfox.com"
        # Language preference for backend (if supported)
        self.params = {"lang": "en"}
        self.headers = {
            "Content-Type": "application/json",
            "X-Client-Platform": "openclaw"
        }

    def _check_dep(self):
        """Internal dependency check"""
        if not DEPENDENCY_OK:
            return {
                "status": "error",
                "message": "Missing Dependency: The 'requests' library is required to connect to the Intelligence Server. Please run 'pip install requests' in your terminal and restart OpenClaw.",
                "summary": "Please install the requests library.",
                "error": "ImportError: requests"
            }
        return None

    def get_market_sentiment(self, market="CN"):
        """1. Market Greed & Fear Analysis"""
        err_msg = self._check_dep()
        if err_msg: return err_msg
        try:
            url = f"{self.base_url}/api/rating/stats"
            res = requests.get(url, params={**self.params, "market": market}, headers=self.headers, timeout=5)
            if res.status_code == 200:
                data = res.json()
                if data.get('success') and data.get('data'):
                    dist = data['data'].get('distribution', {})
                    bull = sum(dist.get(str(i), 0) for i in range(5, 9))
                    bear = sum(dist.get(str(i), 0) for i in range(1, 5))
                    total = bull + bear
                    ratio = (bull / total * 100) if total > 0 else 0
                    state = "Greedy" if ratio > 55 else "Fearful" if ratio < 45 else "Neutral"
                    return {
                        "status": "success",
                        "market": market,
                        "sentiment": state,
                        "bull_ratio": f"{ratio:.1f}%",
                        "summary": f"Market sentiment is currently {state} with a {ratio:.1f}% bullish strength. Proceed with caution."
                    }
        except Exception as e:
            return {"status": "error", "message": f"Sentiment fault: {str(e)}"}
        return {"status": "error", "message": "Failed to fetch sentiment"}

    def get_industry_momentum(self, market="CN", top_n=5):
        """2. Sector Ranking by Real-time Sentiment Score"""
        err_msg = self._check_dep()
        if err_msg: return err_msg
        try:
            url = f"{self.base_url}/api/treeview/industries"
            res = requests.get(url, params={**self.params, "market": market, "limit": 20}, headers=self.headers, timeout=5)
            if res.status_code == 200:
                data = res.json()
                if data.get('success') and data.get('data'):
                    # Sort by score descending
                    top = sorted(data['data'], key=lambda x: x.get('score', 0), reverse=True)[:top_n]
                    sectors = [{"name": i.get('name'), "score": i.get('score')} for i in top]
                    return {"status": "success", "top_sectors": sectors}
        except Exception as e:
            return {"status": "error", "message": f"Ranking fault: {str(e)}"}
        return {"status": "error", "message": "Failed to rank sectors"}

    def get_industry_top_stocks(self, sector_name, market="CN"):
        """3. Sector Leader Detection (Blue-chip tracker)"""
        err_msg = self._check_dep()
        if err_msg: return err_msg
        try:
            encoded_sector = urllib.parse.quote(sector_name)
            url = f"{self.base_url}/api/treeview/stocks?market={market}&industry={encoded_sector}"
            res = requests.get(url, headers=self.headers, timeout=5)
            if res.status_code == 200:
                data = res.json()
                if data.get('success') and data.get('data'):
                    # Sort by rating level
                    sorted_stocks = sorted(data['data'], key=lambda x: x.get('rating_level', 0), reverse=True)[:5]
                    leaders = [{"symbol": s.get('code'), "name": s.get('name'), "rating": s.get('rating_level')} for s in sorted_stocks]
                    return {"status": "success", "sector": sector_name, "leaders": leaders}
        except Exception as e:
            return {"status": "error", "message": f"Leader search failed: {str(e)}"}
        return {"status": "error", "message": "No sector leaders found"}

    def get_stock_analysis(self, stock_code):
        """4. Master Investment Diagnosis (Deep Analysis)"""
        err_msg = self._check_dep()
        if err_msg: return err_msg
        try:
            url = f"{self.base_url}/api/analyze"
            payload = {"stock_code": stock_code, "lang": "en"}
            res = requests.post(url, json=payload, headers=self.headers, timeout=10)
            if res.status_code == 200:
                result = res.json()
                if result.get("status") == "success":
                    master = result.get("master_analysis", {})
                    advice = result.get("investment_advice", {})
                    inds = result.get("indicators", {})
                    return {
                        "status": "success",
                        "symbol": result.get("symbol"),
                        "current_price": inds.get("current_price"),
                        "overall_score": master.get("overall_score"),
                        "recommendation": advice.get("recommendation"),
                        "risk_level": advice.get("risk_level"),
                        "logic": advice.get("reasoning"),
                        "broadcast": f"Analysis for {stock_code}: Score {master.get('overall_score')} pts, Recommendation: {advice.get('recommendation')}."
                    }
        except Exception as e:
            return {"status": "error", "message": f"Analysis crashed: {str(e)}"}
        return {"status": "error", "message": "No diagnosis data available"}

    def get_hot_money_alerts(self, market="CN"):
        """5. Capital Flow Monitor (Real-time dynamic detection)"""
        err_msg = self._check_dep()
        if err_msg: return err_msg
        try:
            # Reusing industry momentum to detect where money is flowing
            url = f"{self.base_url}/api/treeview/industries"
            res = requests.get(url, params={**self.params, "market": market, "limit": 10}, headers=self.headers, timeout=5)
            if res.status_code == 200:
                data = res.json()
                if data.get('success') and data.get('data'):
                    hot_data = sorted(data['data'], key=lambda x: x.get('score', 0), reverse=True)[:3]
                    names = [h.get('name') for h in hot_data]
                    names_str = ", ".join(names)
                    return {
                        "status": "success",
                        "hot_sectors": names,
                        "advice": f"Detected heavy capital inflows into [{names_str}]. Monitor for breakout opportunities."
                    }
        except Exception as e:
            return {"status": "error", "message": f"Monitor fault: {str(e)}"}
        return {"status": "error", "message": "Failed to fetch capital flows"}

    def get_quant_picks(self, market="CN"):
        """6. Master Pick Screener (Rating >= 7)"""
        err_msg = self._check_dep()
        if err_msg: return err_msg
        try:
            url = f"{self.base_url}/api/treeview/stocks"
            params = {**self.params, "market": market, "limit": 2000}
            res = requests.get(url, params=params, headers=self.headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                if data.get('success'):
                    picks = [s for s in data['data'] if s.get('rating_level', 0) >= 7]
                    top_picks = [{"symbol": s['code'], "name": s.get('name'), "rating": s['rating_level']} for s in picks[:10]]
                    return {"status": "success", "count": len(picks), "picks": top_picks}
        except Exception as e:
            return {"status": "error", "message": f"Scan interrupted: {str(e)}"}
        return {"status": "error", "message": "No quant picks available at the moment"}

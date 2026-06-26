"""CVE Database 발굴 (NVD API)"""

import logging
import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta
from typing import List, Dict

from builder.discovery.base import DiscoverySource
from builder.models import DiscoverySource as DS

logger = logging.getLogger('builder-agent.discovery.cve')


class CVEDatabaseSource(DiscoverySource):
    """NVD API에서 최신 CVE 발굴"""

    def __init__(self, config=None):
        super().__init__(config)
        self.lookback_days = config.lookback_days if config else 7
        self.min_score = config.min_score if config else 7.0
        self.severity = config.severity if config else "HIGH"
        self.max_results = config.max_results if config else 20

    def discover(self) -> List[Dict]:
        """최근 고위험 CVE 발굴"""
        if not self.enabled:
            return []

        ideas = []

        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=self.lookback_days)

            url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
            params = urllib.parse.urlencode({
                'resultsPerPage': self.max_results,
                'pubStartDate': start_date.strftime('%Y-%m-%dT00:00:00.000'),
                'pubEndDate': end_date.strftime('%Y-%m-%dT23:59:59.999'),
                'cvssV3Severity': self.severity,
            })

            req = urllib.request.Request(f"{url}?{params}")
            req.add_header('User-Agent', 'Builder-Agent-Discovery/1.0')

            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode())

            for vuln in data.get('vulnerabilities', [])[:self.max_results]:
                cve = vuln['cve']
                cve_id = cve.get('id', 'Unknown')

                # 설명
                descriptions = cve.get('descriptions', [])
                description = next(
                    (d['value'] for d in descriptions if d.get('lang') == 'en'),
                    descriptions[0].get('value', 'No description') if descriptions else 'No description'
                )

                # CVSS 점수
                metrics = cve.get('metrics', {})
                severity = 'Unknown'
                score = 0.0

                if 'cvssMetricV31' in metrics:
                    cvss_data = metrics['cvssMetricV31'][0].get('cvssData', {})
                    severity = cvss_data.get('baseSeverity', 'Unknown')
                    score = cvss_data.get('baseScore', 0.0)
                elif 'cvssMetricV2' in metrics:
                    cvss_data = metrics['cvssMetricV2'][0].get('cvssData', {})
                    score = cvss_data.get('baseScore', 0.0)
                    severity = 'HIGH' if score >= 7.0 else 'MEDIUM' if score >= 4.0 else 'LOW'

                if score >= self.min_score:
                    ideas.append({
                        'title': f"CVE Scanner: {cve_id}",
                        'description': f"Scanner for {description[:150]}",
                        'source': DS.CVE_DATABASE.value,
                        'cve_id': cve_id,
                        'severity': severity,
                        'score': score,
                        'url': f"https://nvd.nist.gov/vuln/detail/{cve_id}",
                        'complexity': 'medium',
                        'priority': 'high' if severity == 'CRITICAL' else 'medium',
                        'discovered_at': datetime.now().isoformat()
                    })

            logger.info("CVE Database: %d ideas found", len(ideas))

        except urllib.error.HTTPError as e:
            logger.warning("CVE API HTTP Error %d: %s", e.code, e.reason)
        except urllib.error.URLError as e:
            logger.warning("CVE API Network Error: %s", e.reason)
        except Exception as e:
            logger.warning("CVE API error: %s", e)

        return ideas

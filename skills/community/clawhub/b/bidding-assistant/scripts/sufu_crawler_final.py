#!/usr/bin/env python3
"""
苏服采采集器 - API直连修复版
绕过UI级联选择问题，直接调用后端API获取数据

API: POST https://js.fwgov.cn:868/purchases/tenders/notice/page
地区代码: 盐南高新区=320992, 经开区=320991
"""
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional

import requests

from crawler import BaseCrawler, DatabaseManager, ProjectExtractor

logger = logging.getLogger(__name__)

API_URL = "https://js.fwgov.cn:868/purchases/tenders/notice/page"

REGION_CONFIG = {
    '盐南高新区': {'code': '320992'},
    '经开区': {'code': '320991'}
}


class SufuCrawlerNew(BaseCrawler):
    """苏服采采集器 - API直连版"""

    SITE_NAME = "苏服采"
    BASE_URL = "https://js.fwgov.cn"

    def crawl(self, start_date: str, end_date: str) -> Dict:
        """采集数据"""
        logger.info(f"开始采集: {self.SITE_NAME} (API直连模式)")

        total_count = 0
        new_count = 0

        for region_name, config in REGION_CONFIG.items():
            try:
                area_code = config['code']
                page = 1
                page_size = 20

                while True:
                    result = self._fetch_page(area_code, "1", page, page_size)

                    if not result or not result.get('success'):
                        logger.warning(f"  页{page}: 获取失败")
                        break

                    records = result.get('result', {}).get('records', [])
                    if not records:
                        break

                    logger.info(f"  {region_name} 页{page}: 获取 {len(records)} 条")

                    for r in records:
                        project = self._parse_record(r, region_name)
                        if self._save_project(project):
                            new_count += 1
                        total_count += 1

                    # 检查是否还有更多
                    total = result.get('result', {}).get('total', 0)
                    if page * page_size >= total:
                        break

                    page += 1
                    time.sleep(0.3)

            except Exception as e:
                logger.error(f"采集 {region_name} 失败: {e}")

        logger.info(f"{self.SITE_NAME} 采集完成: 总计 {total_count} 条, 新增 {new_count} 条")
        return {"total": total_count, "new": new_count}

    def _fetch_page(self, area_code: str, service_type: str = "1", page: int = 1, page_size: int = 20) -> Optional[Dict]:
        """获取单页数据"""
        payload = {
            "samEnterprises": "",
            "biddingStatus": "",
            "itemBudgetStart": "",
            "itemBudgetEnd": "",
            "sort": "",
            "order": "",
            "nameOrunit": "",
            "pageNumber": page,
            "pageSize": page_size,
            "areaCode": [area_code] if area_code else [],
            "serviceType": service_type
        }

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Origin': 'https://js.fwgov.cn',
            'Referer': 'https://js.fwgov.cn/bidding?serviceType=1'
        }

        try:
            resp = requests.post(API_URL, json=payload, headers=headers, timeout=30)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.error(f"请求异常: {e}")
        return None

    def _parse_record(self, record: Dict, region: str) -> Dict:
        """解析单条记录"""
        project_name = record.get('itemName', '')

        # 生成唯一ID
        project_id = ProjectExtractor.generate_id(
            project_name,
            record.get('publishTime', datetime.now().strftime('%Y-%m-%d')),
            self.SITE_NAME
        )
        hash_val = ProjectExtractor.generate_hash({
            'project_name': project_name,
            'publish_date': record.get('publishTime'),
            'source_site': self.SITE_NAME
        })

        return {
            'id': project_id,
            'source_site': self.SITE_NAME,
            'source_url': self.BASE_URL,
            'publish_date': record.get('publishTime', '')[:10] if record.get('publishTime') else datetime.now().strftime('%Y-%m-%d'),
            'project_name': project_name,
            'budget': record.get('itemBudget', 0),
            'detail_url': f"{self.BASE_URL}/bidding details?id={record.get('id', '')}",
            'region': region,
            'purchaser': record.get('procurementUnit', ''),
            'deadline': record.get('tenderEndTime', ''),
            'project_type': '招标公告',
            'raw_content': str(record),
            'hash': hash_val
        }


if __name__ == '__main__':
    # 测试采集
    logging.basicConfig(level=logging.INFO)

    db_manager = DatabaseManager()
    crawler = SufuCrawlerNew(db_manager)
    result = crawler.crawl('', '')
    print(f"采集完成: {result}")
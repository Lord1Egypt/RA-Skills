#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
地址智能分类器 (Address Classifier)
功能：将中国地址按照行政区划进行自动分类
版本：1.0.0
作者：ClawHub Skills
"""

import re
import os
import json
import logging
import csv
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum


class AddressCategory(Enum):
    """地址大类枚举"""
    LOCAL_CITY = "本省本市"      # 目标城市（如贵阳市）
    LOCAL_PROVINCE = "本省外市"  # 省内其他城市
    OTHER_PROVINCE = "外省"      # 其他省份
    INCOMPLETE = "地址不全"      # 信息不完整
    UNKNOWN = "未知"             # 无法识别


@dataclass
class AddressResult:
    """地址分类结果数据类"""
    id: str
    original_address: str
    classified_result: str  # 如：贵州贵阳南明、贵州毕节市、外省四川省
    category: str          # 如：本省本市、本省外市、外省
    province: str          # 省份
    city: str             # 城市
    district: str         # 区县
    is_complete: bool     # 是否完整
    remark: str           # 备注（如补全信息）


class AddressClassifier:
    """
    地址智能分类器

    支持将地址按照以下规则分类：
    1. 本省本市：目标城市（如贵州省贵阳市）下的所有区县
    2. 本省外市：同一省份（如贵州省）内其他城市
    3. 外省：其他省份地址
    4. 地址不全：信息缺失无法分类的地址
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        初始化分类器

        Args:
            config: 配置字典，包含以下可选配置：
                - target_province: 目标省份（默认：贵州省）
                - target_city: 目标城市（默认：贵阳市）
                - target_city_short: 目标城市简称（默认：贵阳）
                - enable_search_completion: 是否启用搜索补全（默认：True）
                - output_format: 输出格式（txt/csv/json，默认：txt）
                - encoding: 文件编码（默认：utf-8）
                - delimiter: 分隔符（默认：\t）
        """
        # 默认配置
        self.config = {
            'target_province': '贵州省',
            'target_city': '贵阳市',
            'target_city_short': '贵阳',
            'enable_search_completion': True,
            'output_format': 'txt',
            'encoding': 'utf-8',
            'delimiter': '\t',
            'log_level': 'INFO',
            'log_file': None  # 如果为None，输出到控制台
        }

        # 更新用户配置
        if config:
            self.config.update(config)

        # 初始化日志
        self._setup_logging()

        # 初始化行政区划数据
        self._init_region_data()

        self.logger.info(f"AddressClassifier initialized with config: {self.config}")

    def _setup_logging(self):
        """配置日志系统"""
        log_level = getattr(logging, self.config['log_level'].upper(), logging.INFO)

        handlers = []
        if self.config['log_file']:
            handlers.append(logging.FileHandler(self.config['log_file'], encoding='utf-8'))
        handlers.append(logging.StreamHandler())

        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=handlers
        )
        self.logger = logging.getLogger(__name__)

    def _init_region_data(self):
        """
        初始化行政区划映射数据
        包含贵州省所有市州及其下辖县区的映射关系
        """
        target_city = self.config['target_city']
        target_city_short = self.config['target_city_short']

        # 目标城市（贵阳）下辖的区县映射
        # 注意：这些区县虽然名为县/市，但属于目标城市管辖
        self.target_city_counties = {
            '开阳县': f'{target_city_short}开阳',
            '息烽县': f'{target_city_short}息烽',
            '修文县': f'{target_city_short}修文',
            '清镇市': f'{target_city_short}清镇'
        }

        # 目标城市主城区
        self.target_city_districts = ['南明', '云岩', '观山湖', '花溪', '乌当', '白云', '小河']

        # 省内其他市州及其下辖县区映射
        self.province_city_map = {
            '毕节市': {
                'counties': ['黔西市', '黔西县', '赫章县', '纳雍县', '织金县', '大方县', '金沙县', '威宁'],
                'short_name': '毕节市'
            },
            '六盘水市': {
                'counties': ['六枝特区', '水城县', '盘州市', '钟山区'],
                'short_name': '六盘水市'
            },
            '安顺市': {
                'counties': ['普定县', '关岭', '镇宁', '紫云', '西秀区', '平坝区'],
                'short_name': '安顺市'
            },
            '遵义市': {
                'counties': ['桐梓县', '绥阳县', '正安县', '道真', '务川', '凤冈县', '湄潭县', 
                           '余庆县', '习水县', '赤水市', '仁怀市', '汇川区', '红花岗区', '播州区'],
                'short_name': '遵义市'
            },
            '铜仁市': {
                'counties': ['德江县', '思南县', '石阡县', '玉屏', '印江', '沿河', '松桃', '万山区', '碧江区'],
                'short_name': '铜仁市'
            },
            '黔东南州': {
                'counties': ['榕江县', '岑巩县', '凯里市', '黄平县', '施秉县', '三穗县', '镇远县',
                           '天柱县', '锦屏县', '剑河县', '台江县', '黎平县', '从江县', '雷山县', '麻江县', '丹寨县'],
                'short_name': '黔东南州'
            },
            '黔南州': {
                'counties': ['贵定县', '瓮安县', '独山县', '平塘县', '罗甸县', '长顺县', 
                           '龙里县', '惠水县', '三都', '荔波县', '都匀市', '福泉市'],
                'short_name': '黔南州'
            },
            '黔西南州': {
                'counties': ['兴义市', '兴仁市', '普安县', '晴隆县', '贞丰县', '望谟县', '册亨县', '安龙县'],
                'short_name': '黔西南州'
            }
        }

        # 搜索补全映射表（用于不完整地址的智能补全）
        # 格式：关键字 -> (完整归属, 省份)
        self.search_completion_map = {
            '西河镇新四村': ('重庆市铜梁区西河镇', '外省重庆市'),
            '善广乡三星村': ('重庆市忠县善广乡', '外省重庆市'),
            '宝龙镇酢房村': ('重庆市大足区宝龙镇', '外省重庆市'),
            '英庄镇张旗营': ('河南省南阳市卧龙区英庄镇', '外省河南省'),
            '隆昌县': ('四川省内江市隆昌市', '外省四川省'),
            '隆昌市': ('四川省内江市隆昌市', '外省四川省')
        }

        # 外省直接识别前缀
        self.other_province_prefixes = {
            '山东省': '外省山东省',
            '四川省': '外省四川省',
            '河南省': '外省河南省',
            '广东省': '外省广东省',
            '重庆市': '外省重庆市'
        }

    def classify(self, address_id: str, address: str) -> AddressResult:
        """
        对单条地址进行分类

        Args:
            address_id: 地址记录ID
            address: 地址字符串

        Returns:
            AddressResult: 分类结果对象
        """
        self.logger.debug(f"Classifying address {address_id}: {address}")

        if not address or not address.strip():
            return self._create_result(address_id, address, "地址不全", 
                                     AddressCategory.INCOMPLETE, "", "", "", False, "空地址")

        addr = address.strip()

        # Step 1: 检查是否为目标城市（本省本市）
        result = self._check_target_city(addr)
        if result:
            return self._create_result(address_id, addr, result['classified'], 
                                     AddressCategory.LOCAL_CITY, 
                                     self.config['target_province'],
                                     self.config['target_city'],
                                     result['district'], True, result.get('remark', ''))

        # Step 2: 检查是否为省内其他城市（本省外市）
        result = self._check_province_other_cities(addr)
        if result:
            return self._create_result(address_id, addr, result['classified'],
                                     AddressCategory.LOCAL_PROVINCE,
                                     self.config['target_province'],
                                     result['city'], "", True, "")

        # Step 3: 检查是否为外省
        result = self._check_other_provinces(addr)
        if result:
            return self._create_result(address_id, addr, result['classified'],
                                     AddressCategory.OTHER_PROVINCE,
                                     result['province'], "", "", True, 
                                     result.get('remark', ''))

        # Step 4: 地址不全检查
        if self._is_incomplete_address(addr):
            return self._create_result(address_id, addr, "地址不全",
                                     AddressCategory.INCOMPLETE, "", "", "", False,
                                     "地址信息过于简略")

        # 无法识别
        return self._create_result(address_id, addr, f"未知-{addr[:20]}",
                                 AddressCategory.UNKNOWN, "", "", "", False,
                                 "无法识别的地址格式")

    def _check_target_city(self, addr: str) -> Optional[Dict]:
        """
        检查是否为目标城市（本省本市）的地址
        """
        target_province = self.config['target_province']
        target_city = self.config['target_city']
        target_city_short = self.config['target_city_short']

        # 检查目标城市的县/县级市（如开阳县、清镇市）
        for county_key, county_value in self.target_city_counties.items():
            if county_key in addr:
                return {
                    'classified': f"{target_province[:2]}{county_value}",
                    'district': county_key.replace('县', '').replace('市', ''),
                    'remark': f"{target_city}下辖{county_key}"
                }

        # 检查目标城市主城区
        if f'{target_province}{target_city}' in addr:
            # 提取具体区县
            pattern = rf"{target_city}(.*?)(?:区|县|市)"
            match = re.search(pattern, addr)
            if match:
                district = match.group(1)
                return {
                    'classified': f"{target_province[:2]}{target_city_short}{district}",
                    'district': district,
                    'remark': ''
                }
            else:
                return {
                    'classified': f"{target_province[:2]}{target_city_short}",
                    'district': '',
                    'remark': '未识别到具体区县'
                }

        return None

    def _check_province_other_cities(self, addr: str) -> Optional[Dict]:
        """
        检查是否为省内其他城市（本省外市）的地址
        """
        target_province = self.config['target_province']

        if target_province not in addr:
            return None

        # 检查各个市州
        for city_name, city_info in self.province_city_map.items():
            # 直接匹配市州名称
            if city_name in addr:
                return {
                    'classified': f"{target_province[:2]}{city_info['short_name']}",
                    'city': city_name
                }

            # 匹配下辖县区
            for county in city_info['counties']:
                if county in addr:
                    return {
                        'classified': f"{target_province[:2]}{city_info['short_name']}",
                        'city': city_name,
                        'remark': f"通过下辖地区{county}识别"
                    }

        return None

    def _check_other_provinces(self, addr: str) -> Optional[Dict]:
        """
        检查是否为外省地址
        """
        # 1. 直接匹配外省前缀
        for prefix, classified in self.other_province_prefixes.items():
            if addr.startswith(prefix):
                # 对于河南省焦作市这种简短地址，需要检查完整性
                if prefix == '河南省' and (addr == '河南省焦作市' or len(addr) <= 8):
                    return None  # 返回None让后续流程标记为地址不全
                return {
                    'classified': classified,
                    'province': prefix.replace('省', '').replace('市', '')
                }

        # 2. 搜索补全（针对不完整的外省地址）
        if self.config['enable_search_completion']:
            for keyword, (actual_location, classified) in self.search_completion_map.items():
                if keyword in addr:
                    return {
                        'classified': classified,
                        'province': classified.replace('外省', ''),
                        'remark': f"通过搜索补全：实际归属为{actual_location}"
                    }

        return None

    def _is_incomplete_address(self, addr: str) -> bool:
        """
        判断地址是否信息不全
        """
        # 长度检查
        if len(addr) < 8:
            return True

        # 仅有省市名，无具体区县或街道
        if addr in ['河南省焦作市'] or len(addr) <= 8:
            return True

        # 有乡镇村名但无省市信息（且未触发补全）
        if ('镇' in addr or '乡' in addr or '村' in addr) and '省' not in addr:
            return True

        return False

    def _create_result(self, address_id: str, original: str, classified: str,
                      category: AddressCategory, province: str, city: str,
                      district: str, is_complete: bool, remark: str) -> AddressResult:
        """创建结果对象"""
        return AddressResult(
            id=address_id,
            original_address=original,
            classified_result=classified,
            category=category.value,
            province=province,
            city=city,
            district=district,
            is_complete=is_complete,
            remark=remark
        )

    def process_file(self, input_path: str, output_path: str) -> Dict:
        """
        处理文件中的地址数据

        Args:
            input_path: 输入文件路径（制表符分隔，包含id和address两列）
            output_path: 输出文件路径

        Returns:
            Dict: 处理统计信息
        """
        self.logger.info(f"Processing file: {input_path}")

        results = []
        stats = {
            'total': 0,
            '本省本市': 0,
            '本省外市': 0,
            '外省': 0,
            '地址不全': 0,
            '未知': 0
        }

        try:
            # 读取输入文件
            with open(input_path, 'r', encoding=self.config['encoding']) as f:
                # 跳过表头
                header = f.readline()

                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split('\t')
                    if len(parts) >= 2:
                        address_id = parts[0]
                        address = parts[1]

                        result = self.classify(address_id, address)
                        results.append(result)
                        stats[result.category] += 1
                        stats['total'] += 1

            # 写入输出文件
            self._write_output(results, output_path)

            self.logger.info(f"Processing completed. Stats: {stats}")
            return stats

        except Exception as e:
            self.logger.error(f"Error processing file: {e}")
            raise

    def _write_output(self, results: List[AddressResult], output_path: str):
        """
        写入输出文件
        """
        format_type = self.config['output_format'].lower()
        delimiter = self.config['delimiter']

        if format_type == 'csv':
            self._write_csv(results, output_path)
        elif format_type == 'json':
            self._write_json(results, output_path)
        else:
            self._write_txt(results, output_path, delimiter)

    def _write_txt(self, results: List[AddressResult], output_path: str, delimiter: str):
        """写入TXT格式（制表符分隔）"""
        with open(output_path, 'w', encoding=self.config['encoding']) as f:
            # 写入表头
            f.write(f"id{delimiter}原地址{delimiter}分类结果{delimiter}大类标识{delimiter}省份{delimiter}城市{delimiter}区县{delimiter}备注\n")

            for result in results:
                line = f"{result.id}{delimiter}{result.original_address}{delimiter}"                        f"{result.classified_result}{delimiter}{result.category}{delimiter}"                        f"{result.province}{delimiter}{result.city}{delimiter}"                        f"{result.district}{delimiter}{result.remark}\n"
                f.write(line)

    def _write_csv(self, results: List[AddressResult], output_path: str):
        """写入CSV格式"""
        with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', '原地址', '分类结果', '大类标识', '省份', '城市', '区县', '是否完整', '备注'])

            for result in results:
                writer.writerow([
                    result.id, result.original_address, result.classified_result,
                    result.category, result.province, result.city, result.district,
                    '是' if result.is_complete else '否', result.remark
                ])

    def _write_json(self, results: List[AddressResult], output_path: str):
        """写入JSON格式"""
        data = [asdict(r) for r in results]
        with open(output_path, 'w', encoding=self.config['encoding']) as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def batch_classify(self, addresses: List[Tuple[str, str]]) -> List[AddressResult]:
        """
        批量分类地址

        Args:
            addresses: 地址列表，每项为(id, address)元组

        Returns:
            List[AddressResult]: 分类结果列表
        """
        results = []
        for address_id, address in addresses:
            result = self.classify(address_id, address)
            results.append(result)
        return results


# 使用示例
if __name__ == "__main__":
    # 示例1：使用默认配置
    classifier = AddressClassifier()

    # 示例2：使用自定义配置
    config = {
        'target_province': '贵州省',
        'target_city': '贵阳市',
        'target_city_short': '贵阳',
        'output_format': 'csv',
        'log_level': 'DEBUG'
    }
    classifier = AddressClassifier(config)

    # 单条分类示例
    test_cases = [
        ("202020001", "贵州省贵阳市南明区沙冲南路226号3栋3单元3楼1号"),
        ("202020018", "西河镇新四村11组32号"),
        ("202020032", "贵州省仁怀市长岗镇丰岩村冉家坡组"),
        ("202020206", "河南省焦作市")
    ]

    print("\n单条分类测试：")
    print("-" * 100)
    for addr_id, addr in test_cases:
        result = classifier.classify(addr_id, addr)
        print(f"ID: {result.id}")
        print(f"  原地址: {result.original_address}")
        print(f"  分类结果: {result.classified_result}")
        print(f"  大类: {result.category}")
        print(f"  备注: {result.remark}")
        print()

#!/usr/bin/env python3

import sys
import os
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd
from datetime import datetime
import logging

# 导入特征识别标准模块
sys.path.insert(0, os.path.dirname(__file__))
from feature_extraction import FeatureExtractor

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PersonaInsightAnalyzerV9:
    """v9.0 严格流程分析器"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.feature_extractor = FeatureExtractor()
        logger.info(f"初始化 PersonaInsightAnalyzerV9(严格流程版)")
        logger.info(f"输出目录: {self.output_dir}")
    
    def load_data(self, file_path: str) -> Dict[str, pd.DataFrame]:
        """加载 Excel 或 CSV 数据"""
        file_path = str(file_path)
        logger.info(f"开始加载数据: {file_path}")
        
        if file_path.endswith(('.xlsx', '.xls')):
            excel_file = pd.ExcelFile(file_path)
            sheets = {}
            for sheet_name in excel_file.sheet_names:
                sheets[sheet_name] = pd.read_excel(file_path, sheet_name=sheet_name)
            logger.info(f"Excel 加载完成,共 {len(sheets)} 个 sheet")
            return sheets
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
            logger.info(f"CSV 加载完成,共 {len(df)} 行")
            return {'data': df}
        else:
            raise ValueError("仅支持 .xlsx、.xls 和 .csv 格式")
    
    def _find_column(self, df: pd.DataFrame, possible_names: List[str]) -> Optional[str]:
        """在 DataFrame 中查找列"""
        for name in possible_names:
            if name in df.columns:
                return name
            for col in df.columns:
                if col.lower() == name.lower():
                    return col
        return None
    
    def analyze_dimension(self, dimension_name: str, df: pd.DataFrame) -> Dict[str, Any]:
        """分析单个维度"""
        logger.info(f"\n=== 开始分析维度: {dimension_name} ===")
        
        result = {
            'dimension': dimension_name,
            'total_items': len(df),
            'features': [],
            'core_count': 0,
            'avg_tgi': 0,
            'max_tgi': 0,
            'analysis_steps': {}  # 新增:存储六步分析过程
        }
        
        # 自动列名识别
        tgi_col = self._find_column(df, ['tgi', 'TGI', 'index', '指数'])
        label_col = self._find_column(df, ['二级标签', '标签', '特征', '名称', '一级标签', 'name', 'label'])
        coverage_col = self._find_column(df, ['占比', 'coverage', '比例', 'percentage', '百分比'])
        
        if not tgi_col or tgi_col not in df.columns:
            logger.warning(f"维度 {dimension_name}: 未找到 TGI 列,跳过")
            return result
        
        # 准备特征列表
        features_list = []
        for idx, (_, row) in enumerate(df.iterrows()):
            feature_name = str(row[label_col]) if label_col and label_col in df.columns else f"特征{idx}"
            tgi_val = row[tgi_col]
            
            if not isinstance(tgi_val, (int, float)) or pd.isna(tgi_val):
                continue
            
            coverage_val = 0
            if coverage_col and coverage_col in df.columns:
                cov = row[coverage_col]
                if isinstance(cov, (int, float)) and not pd.isna(cov):
                    coverage_val = float(cov)
            
            features_list.append({
                'name': feature_name,
                'tgi': float(tgi_val),
                'coverage': coverage_val,
            })
        
        if not features_list:
            logger.warning(f"维度 {dimension_name}: 无有效特征")
            return result
        
        # 使用特征提取器并记录六步过程
        core_features, stats = self.feature_extractor.extract_dimension_features(
            dimension_name, features_list
        )
        
        # 记录六步分析过程
        result['analysis_steps'] = self._generate_analysis_steps(
            dimension_name, features_list, core_features, stats
        )
        
        result['features'] = core_features
        result['core_count'] = len(core_features)
        result['total_valid'] = stats.get('valid', 0)
        result['avg_tgi'] = stats.get('avg_tgi', 0)
        result['max_tgi'] = stats.get('max_tgi', 0)
        
        logger.info(f"分析完成: {len(core_features)} 条核心特征")
        return result
    
    def _generate_analysis_steps(self, dimension_name: str, all_features: List[Dict], 
                                 core_features: List[Dict], stats: Dict) -> Dict[str, str]:
        """生成六步完整分析过程"""
        steps = {}
        
        # 步骤1:排序
        sorted_features = sorted(all_features, key=lambda x: (-x['tgi'], -x['coverage']))
        steps['step1_sort'] = f"按TGI降序排序,共{len(sorted_features)}条特征"
        
        # 步骤2:筛选TGI≥1.0
        valid_features = [f for f in sorted_features if f['tgi'] >= 1.0]
        steps['step2_filter'] = f"筛选TGI≥1.0,保留{len(valid_features)}条有效特征(占比{len(valid_features)/len(sorted_features)*100:.1f}%)"
        
        # 步骤3:取前40%
        core_count = len(core_features)
        steps['step3_top40'] = f"取前40%,保留{core_count}条核心特征"
        
        # 步骤4:并列特征识别
        parallel_count = sum(1 for f in core_features if '并列' in f.get('note', ''))
        steps['step4_parallel'] = f"识别并列特征,发现{parallel_count}组并列特征" if parallel_count > 0 else "未发现并列特征"
        
        # 步骤5:互斥关系处理
        steps['step5_exclusive'] = "已处理互斥关系"
        
        # 步骤6:无区分度特征排除
        steps['step6_discrimination'] = "已排除无区分度特征"
        
        return steps
    
    def analyze_all_dimensions(self, data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """分析所有维度"""
        logger.info(f"\n{'='*60}")
        logger.info(f"开始全维度分析(使用 v9.0 严格流程)")
        logger.info(f"{'='*60}\n")
        
        all_dimensions = {}
        for sheet_name, df in data.items():
            logger.info(f"\n处理 sheet: {sheet_name}")
            result = self.analyze_dimension(sheet_name, df)
            all_dimensions[sheet_name] = result
        
        return all_dimensions
    
    def generate_persona_summary(self, dimensions: Dict[str, Any]) -> Dict[str, str]:
        """
        生成用户画像(详细的一句话核心特征)
        
        格式:年龄段+性别+消费力+核心兴趣+地域特征+生活方式+设备偏好等
        """
        # 提取各维度Top特征
        age_feature = ""
        gender_feature = ""
        consumption_feature = ""
        interest_features = []
        geo_feature = ""
        lifestyle_features = []
        device_feature = ""
        
        for dim_name, dim_result in dimensions.items():
            if not dim_result['features']:
                continue
            
            top_feature = dim_result['features'][0]['name']
            
            # 识别年龄
            if '年龄' in dim_name or '基础标签' in dim_name:
                for feat in dim_result['features'][:3]:
                    if '岁' in feat['name'] or '年龄' in feat['name']:
                        age_feature = feat['name']
                        break
            
            # 识别性别
            if '性别' in dim_name or '基础标签' in dim_name:
                for feat in dim_result['features'][:3]:
                    if '男' in feat['name'] or '女' in feat['name']:
                        gender_feature = feat['name']
                        break
            
            # 识别消费力
            if '消费' in dim_name or '品类' in dim_name:
                consumption_feature = top_feature
            
            # 识别兴趣
            if '兴趣' in dim_name:
                interest_features.extend([f['name'] for f in dim_result['features'][:3]])
            
            # 识别地域
            if '地域' in dim_name or '城市' in dim_name or '省份' in dim_name:
                geo_feature = top_feature
            
            # 识别生活方式
            if '场景' in dim_name or '应用' in dim_name:
                lifestyle_features.extend([f['name'] for f in dim_result['features'][:2]])
            
            # 识别设备
            if '手机' in dim_name or '设备' in dim_name:
                device_feature = top_feature
        
        # 生成详细的一句话核心特征
        parts = []
        if age_feature:
            parts.append(age_feature)
        if gender_feature:
            parts.append(gender_feature)
        if consumption_feature:
            parts.append(f"关注{consumption_feature}")
        if interest_features:
            parts.append(f"热衷{'/'.join(interest_features[:2])}")
        if geo_feature:
            parts.append(f"活跃于{geo_feature}")
        if lifestyle_features:
            parts.append(f"注重{'/'.join(lifestyle_features[:2])}")
        if device_feature:
            parts.append(f"使用{device_feature}")
        
        # 如果没有提取到足够信息,使用Top特征
        if len(parts) < 3:
            top_features = []
            for dim_result in dimensions.values():
                if dim_result['features']:
                    top_features.extend([f['name'] for f in dim_result['features'][:2]])
            parts = top_features[:6]
        
        core_feature = '、'.join(parts) + "的用户群体"
        
        # 提炼核心定位
        positioning = self._extract_positioning_detailed(dimensions)
        
        return {
            'core_feature': core_feature,
            'positioning': positioning
        }
    
    def _extract_positioning_detailed(self, dimensions: Dict) -> str:
        """提炼核心定位标签(基于多维度特征)"""
        # 收集所有Top特征
        all_top_features = []
        for dim_result in dimensions.values():
            if dim_result['features']:
                all_top_features.extend([f['name'] for f in dim_result['features'][:3]])
        
        feature_text = ' '.join(all_top_features)
        
        # 分析特征类型
        has_sports = any(kw in feature_text for kw in ['体育', '运动', '健身', '赛事'])
        has_travel = any(kw in feature_text for kw in ['旅游', '出行', '户外'])
        has_tech = any(kw in feature_text for kw in ['科技', '数码', '手机', '电脑'])
        has_family = any(kw in feature_text for kw in ['亲子', '育儿', '家庭', '母婴'])
        has_finance = any(kw in feature_text for kw in ['金融', '理财', '投资'])
        has_car = any(kw in feature_text for kw in ['汽车', '自驾', '车'])
        
        # 根据特征组合生成定位
        if has_sports and has_travel:
            return "都市运动旅行爱好者"
        elif has_sports and has_tech:
            return "都市运动科技男"
        elif has_car and has_travel:
            return "自驾旅行生活家"
        elif has_family and has_tech:
            return "科技育儿新生代"
        elif has_finance and has_tech:
            return "理财科技精英"
        elif has_sports:
            return "运动健康追求者"
        elif has_travel:
            return "旅行生活方式驱动型用户"
        elif has_tech:
            return "科技数码爱好者"
        elif has_family:
            return "品质育儿家庭用户"
        else:
            return "品质生活追求者"
    
    def generate_geo_insights(self, dimensions: Dict[str, Any]) -> Optional[str]:
        """生成地域深耕方向"""
        geo_dim = None
        for dim_name, dim_result in dimensions.items():
            if '地域' in dim_name or '城市' in dim_name or '省份' in dim_name:
                if dim_result['features']:
                    geo_dim = dim_result
                    break
        
        if not geo_dim:
            return None
        
        features = geo_dim['features']
        
        # 核心省份: TGI > 1.5 且占比 > 3%
        core_provinces = [f for f in features if f.get('tgi', 0) > 1.5 and f.get('coverage', 0) > 0.03]
        
        # 潜力城市: TGI > 1.5 且占比 1-3%
        potential_cities = [f for f in features if f.get('tgi', 0) > 1.5 and 0.01 <= f.get('coverage', 0) <= 0.03]
        
        # 低优先级: TGI < 1
        low_priority = [f for f in features if f.get('tgi', 0) < 1.0]
        
        result = "## 二、地域深耕方向\n\n"
        
        if core_provinces:
            provinces = '、'.join([f['name'] for f in core_provinces[:5]])
            result += f"**核心省份**: {provinces}\n"
            result += f"(TGI高且占比大,优先布局投放)\n\n"
        
        if potential_cities:
            cities = '、'.join([f['name'] for f in potential_cities[:5]])
            result += f"**潜力城市**: {cities}\n"
            result += f"(TGI高但当前占比适中,重点渗透)\n\n"
        
        if low_priority:
            regions = '、'.join([f['name'] for f in low_priority[:3]])
            result += f"**低优先级地区**: {regions}\n"
            result += f"(TGI<1,建议减少投入或暂停)\n\n"
        
        return result
    
    def generate_dimension_analysis_detailed(self, dimensions: Dict[str, Any]) -> str:
        """
        生成各维度详细分析(严格按照六步流程)
        """
        result = "## 三、各维度详细分析\n\n"
        
        # 按最高TGI排序
        sorted_dims = sorted(
            dimensions.items(),
            key=lambda x: x[1].get('max_tgi', 0),
            reverse=True
        )
        
        for dim_name, dim_result in sorted_dims:
            if not dim_result['features']:
                continue
            
            result += f"### {dim_name}维度\n\n"
            
            # 核心特征列表(使用三步法筛选后的所有核心特征)
            core_features = dim_result['features']
            result += f"**核心特征列表**({len(core_features)}条):\n\n"
            for i, feat in enumerate(core_features, 1):
                tgi = feat.get('tgi', 0)
                coverage = feat.get('coverage', 0)
                if coverage:
                    result += f"{i}. {feat['name']}(TGI {tgi:.2f}, 占比 {coverage:.2%})\n"
                else:
                    result += f"{i}. {feat['name']}(TGI {tgi:.2f})\n"
            
            result += "\n"
            
            # 判断理由
            result += "**判断理由**:\n\n"
            if dim_result['max_tgi'] > 0 and dim_result['avg_tgi'] > 0:
                ratio = dim_result['max_tgi'] / dim_result['avg_tgi']
                if ratio > 1.5:
                    result += f"该维度特征聚焦度高(最高TGI {dim_result['max_tgi']:.2f} 是平均值 {dim_result['avg_tgi']:.2f} 的 {ratio:.1f} 倍),用户在此维度有明显的特征集中。\n\n"
                else:
                    result += f"该维度特征分布相对均衡(最高TGI {dim_result['max_tgi']:.2f},平均值 {dim_result['avg_tgi']:.2f}),用户呈现多元化特征。\n\n"
            
            # 数据分布说明
            result += "**数据分布说明**:\n\n"
            result += f"该维度共包含 {dim_result['total_items']} 条标签数据,其中 {dim_result['total_valid']} 条有效特征(TGI ≥ 1.0),"
            result += f"筛选后保留 {dim_result['core_count']} 条核心特征(前40%),最高TGI {dim_result['max_tgi']:.2f},"
            result += f"平均TGI {dim_result['avg_tgi']:.2f}。\n\n"
        
        return result
    
    def generate_strategy_suggestions(self, dimensions: Dict[str, Any], persona: Dict[str, str]) -> str:
        """生成综合策略建议"""
        top_features = []
        for dim_name, dim_result in dimensions.items():
            if dim_result['features']:
                top_features.extend(dim_result['features'][:5])
        
        top_features.sort(key=lambda x: x.get('tgi', 0), reverse=True)
        
        result = "## 四、综合策略建议\n\n"
        
        # 产品定位
        result += "### 【产品定位】\n\n"
        result += f"面向{persona['positioning']}的专业产品和服务\n\n"
        result += "**强调**: 品质保证、专业服务、便捷高效、价值认同\n\n"
        
        # 渠道布局策略
        result += "### 【渠道布局策略】\n\n"
        
        channels = self._recommend_channels(top_features)
        for channel_type, channel_items in channels.items():
            result += f"**{channel_type}**:\n\n"
            for item in channel_items:
                result += f"- {item}\n"
            result += "\n"
        
        # 内容营销策略
        result += "### 【内容营销策略】\n\n"
        
        content_strategies = self._recommend_content(top_features)
        for strategy_type, strategy_items in content_strategies.items():
            result += f"**{strategy_type}**:\n\n"
            for item in strategy_items:
                result += f"- {item}\n"
            result += "\n"
        
        return result
    
    def _recommend_channels(self, features: List[Dict]) -> Dict[str, List[str]]:
        """根据特征推荐渠道(详细格式)"""
        channels = {}
        
        feature_names = ' '.join([f['name'] for f in features[:10]])
        
        # 根据特征识别垂直平台
        if '汽车' in feature_names or '自驾' in feature_names:
            channels['汽车垂直平台'] = [
                '汽车之家、懂车帝、易车网等汽车资讯平台进行内容营销',
                '4S店、汽车展会等线下场景进行体验式营销',
                '汽车社区、车友会等进行精准投放'
            ]
        
        if '体育' in feature_names or '运动' in feature_names or '健身' in feature_names:
            channels['体育健康专业平台'] = [
                '央视体育、腾讯体育等体育资讯平台进行内容营销',
                '健身中心、运动场馆等线下场景进行体验式营销',
                'Keep、咕咚等运动健康APP进行精准投放'
            ]
        
        if '旅游' in feature_names or '户外' in feature_names:
            channels['旅游出行平台'] = [
                '携程、去哪儿、马蜂窝等旅游平台进行内容营销',
                '景区、民宿等线下场景进行体验式营销',
                '旅游攻略、户外社区等进行精准投放'
            ]
        
        if '金融' in feature_names or '理财' in feature_names or '保险' in feature_names:
            channels['金融理财平台'] = [
                '雪球、东方财富等金融资讯平台进行内容营销',
                '银行、证券公司等线下场景进行体验式营销',
                '支付宝理财、微信理财通等进行精准投放'
            ]
        
        if '母婴' in feature_names or '育儿' in feature_names or '亲子' in feature_names:
            channels['母婴垂直平台'] = [
                '宝宝树、妈妈网等母婴社区进行内容营销',
                '母婴店、早教中心等线下场景进行体验式营销',
                '育儿APP、亲子平台等进行精准投放'
            ]
        
        # 综合电商平台(必选)
        channels['综合电商平台'] = [
            '淘宝、京东、拼多多等主流电商平台是核心销售渠道',
            '数码产品、食品饮料、体育用品等品类是重点',
            '优惠返利、二手电商等渠道也有一定价值'
        ]
        
        # 社交电商(必选)
        channels['社交电商'] = [
            '微信、小红书等社交平台进行口碑营销',
            '抖音、快手等短视频平台进行内容种草',
            'KOL/KOC合作,打造真实使用场景'
        ]
        
        return channels
    
    def _recommend_content(self, features: List[Dict]) -> Dict[str, List[str]]:
        """根据特征推荐内容策略(详细格式)"""
        strategies = {}
        
        feature_names = ' '.join([f['name'] for f in features[:10]])
        
        # 根据特征识别专业知识类型
        if '汽车' in feature_names or '自驾' in feature_names:
            strategies['汽车专业知识'] = [
                '自驾游攻略、车辆保养技巧、汽车评测对比等专业内容',
                '汽车装备推荐、驾驶技巧分享等实用内容'
            ]
        
        if '体育' in feature_names or '运动' in feature_names or '健身' in feature_names:
            strategies['体育健康专业知识'] = [
                '运动健康科普、健身教程、赛事解读等专业内容',
                '运动装备评测、健康饮食建议等实用内容'
            ]
        
        if '旅游' in feature_names or '户外' in feature_names:
            strategies['旅游出行资讯'] = [
                '周边游推荐、户外运动教程、景点打卡攻略等专业内容',
                '旅游装备推荐、出行攻略分享等实用内容'
            ]
        
        if '金融' in feature_names or '理财' in feature_names or '保险' in feature_names:
            strategies['金融理财指导'] = [
                '投资理财技巧、保险规划建议、消费优惠信息等专业内容',
                '理财产品评测、财务规划建议等实用内容'
            ]
        
        if '母婴' in feature_names or '育儿' in feature_names or '亲子' in feature_names:
            strategies['母婴育儿知识'] = [
                '育儿科普、早教教程、儿童健康等专业内容',
                '母婴产品评测、育儿经验分享等实用内容'
            ]
        
        if '数码' in feature_names or '科技' in feature_names or '手机' in feature_names:
            strategies['科技数码资讯解读'] = [
                '数码产品评测、科技趋势分析、AI工具使用教程',
                '智能设备推荐、性价比产品对比'
            ]
        
        # 用户体验分享(必选)
        strategies['用户体验分享'] = [
            '真实用户运动打卡、健身成果展示',
            '产品使用体验、生活方式分享',
            '家庭生活场景(学龄儿童教育、有车生活等)'
        ]
        
        return strategies
    
    def generate_deep_analysis(self, dimensions: Dict[str, Any]) -> str:
        """生成深度分析建议"""
        result = "## 五、深度分析建议\n\n"
        
        # 单维度深度分析
        result += "### 单维度深度分析建议\n\n"
        
        sorted_dims = sorted(
            [(name, data) for name, data in dimensions.items() if data['features']],
            key=lambda x: x[1]['max_tgi'],
            reverse=True
        )
        
        priority_levels = ['高', '中', '低']
        for i, (dim_name, dim_data) in enumerate(sorted_dims[:3]):
            priority = priority_levels[min(i, 2)]
            result += f"**{i+1}. {dim_name}维度**(优先级: {priority})\n\n"
            result += f"- **分析价值**: 最高TGI {dim_data['max_tgi']:.2f},具有显著区分度\n"
            result += f"- **分析方法**: 深入挖掘Top特征的用户行为模式和消费偏好\n\n"
        
        # 交叉维度分析
        result += "### 交叉维度分析建议\n\n"
        
        if len(sorted_dims) >= 2:
            combinations = [
                (sorted_dims[0][0], sorted_dims[1][0]),
                (sorted_dims[0][0], sorted_dims[2][0]) if len(sorted_dims) > 2 else None,
                (sorted_dims[1][0], sorted_dims[2][0]) if len(sorted_dims) > 2 else None,
            ]
            
            for i, combo in enumerate([c for c in combinations if c], 1):
                result += f"**{i}. {combo[0]} × {combo[1]}**\n\n"
                result += f"- **洞察价值**: 发现{combo[0]}和{combo[1]}的关联模式\n"
                result += f"- **应用场景**: 精准人群细分和个性化营销策略\n\n"
        
        # 优先级排序说明
        result += "### 优先级排序说明\n\n"
        result += "- **高优先级**: 最高TGI维度,商业价值大,建议优先分析\n"
        result += "- **中优先级**: 次高TGI维度,有一定价值,可后续跟进\n"
        result += "- **低优先级**: 其他维度,作为补充分析\n\n"
        
        return result
    
    def generate_markdown_report(self, dimensions: Dict[str, Any], persona_name: str = "") -> str:
        """生成完整的 Markdown 分析报告"""
        logger.info("\n开始生成完整 Markdown 报告...")
        
        if not persona_name:
            persona_name = "目标人群"
        
        # 生成用户画像
        persona = self.generate_persona_summary(dimensions)
        
        # 开始构建报告
        report = f"# 📊 {persona_name}洞察分析报告\n\n"
        report += f"> 本报告使用标准特征识别算法 v9.0 生成,严格按照六步流程输出\n\n"
        report += f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report += "---\n\n"
        
        # 一、用户画像
        report += "## 一、用户画像\n\n"
        report += f"**一句话核心特征**: {persona['core_feature']}\n\n"
        report += f"**提炼核心定位**: {persona['positioning']}\n\n"
        
        # 二、地域深耕方向(如有)
        geo_insights = self.generate_geo_insights(dimensions)
        if geo_insights:
            report += geo_insights
        
        # 三、各维度详细分析(严格六步流程)
        report += self.generate_dimension_analysis_detailed(dimensions)
        
        # 四、综合策略建议
        report += self.generate_strategy_suggestions(dimensions, persona)
        
        # 五、深度分析建议
        report += self.generate_deep_analysis(dimensions)
        
        logger.info("Markdown 报告生成完成")
        return report
    
    def save_report(self, report_content: str, filename: str) -> Path:
        """保存报告到文件"""
        filepath = self.output_dir / filename
        filepath.write_text(report_content, encoding='utf-8')
        logger.info(f"报告已保存: {filepath}")
        return filepath
    
    def process(self, file_path: str, persona_name: str = "") -> Path:
        """完整分析流程"""
        # 加载数据
        data = self.load_data(file_path)
        
        # 分析所有维度
        dimensions = self.analyze_all_dimensions(data)
        
        # 生成完整报告
        report_content = self.generate_markdown_report(dimensions, persona_name)
        
        # 保存报告
        if not persona_name:
            persona_name = Path(file_path).stem
        
        filename = f"{persona_name}_完整分析报告_v9.0.md"
        report_path = self.save_report(report_content, filename)
        
        logger.info(f"\n{'='*60}")
        logger.info(f"✅ 分析完成!")
        logger.info(f"{'='*60}")
        logger.info(f"报告已保存到: {report_path}")
        
        return report_path


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="DMP 人群洞察分析(v9.0 严格流程版)"
    )
    parser.add_argument("file", help="数据文件路径(Excel/CSV)")
    parser.add_argument("--name", "-n", help="人群名称", default="")
    parser.add_argument("--output", "-o", help="输出目录", default="reports")
    
    args = parser.parse_args()
    
    # 创建分析器并处理
    analyzer = PersonaInsightAnalyzerV9(output_dir=args.output)
    analyzer.process(args.file, args.name)


if __name__ == '__main__':
    main()

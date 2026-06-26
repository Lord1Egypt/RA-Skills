#!/usr/bin/env python3
"""
智能技术栈推荐系统
根据项目需求和约束条件，推荐最合适的技术栈
"""

import os
import json
import re
from datetime import datetime

class TechStackRecommender:
    def __init__(self):
        self.tech_stack_data = {
            'frontend': {
                'react': {
                    'description': 'React 是一个用于构建用户界面的 JavaScript 库',
                    'pros': ['组件化开发', '虚拟DOM', '丰富的生态系统', '适合大型应用'],
                    'cons': ['学习曲线较陡', '需要额外的状态管理库'],
                    'use_cases': ['单页应用', '复杂的用户界面', '需要高性能的应用'],
                    'popularity': 95,
                    'community': 90,
                    'maintenance': 85
                },
                'vue': {
                    'description': 'Vue 是一个渐进式 JavaScript 框架',
                    'pros': ['易于学习', '双向数据绑定', '轻量级', '文档完善'],
                    'cons': ['生态系统相对较小', '大型项目经验较少'],
                    'use_cases': ['中小型应用', '快速原型开发', '需要简单上手的场景'],
                    'popularity': 85,
                    'community': 80,
                    'maintenance': 85
                },
                'angular': {
                    'description': 'Angular 是一个由 Google 维护的前端框架',
                    'pros': ['完整的框架', 'TypeScript 支持', '强大的 CLI', '适合大型团队'],
                    'cons': ['学习曲线陡峭', '体积较大', '更新频繁'],
                    'use_cases': ['大型企业应用', '需要严格架构的项目', '团队协作项目'],
                    'popularity': 75,
                    'community': 70,
                    'maintenance': 90
                },
                'svelte': {
                    'description': 'Svelte 是一个构建用户界面的全新方法',
                    'pros': ['编译时优化', '更小的 bundle 体积', '简洁的语法', '响应式系统'],
                    'cons': ['生态系统较小', '企业采用率较低', '社区支持有限'],
                    'use_cases': ['性能敏感的应用', '小型项目', '快速开发'],
                    'popularity': 65,
                    'community': 60,
                    'maintenance': 75
                }
            },
            'backend': {
                'nodejs': {
                    'description': 'Node.js 是基于 Chrome V8 引擎的 JavaScript 运行环境',
                    'pros': ['使用 JavaScript', '非阻塞 I/O', '丰富的包生态', '适合实时应用'],
                    'cons': ['单线程模型', '回调地狱', '内存使用较高'],
                    'use_cases': ['实时应用', 'API 开发', '微服务', '全栈 JavaScript'],
                    'popularity': 90,
                    'community': 85,
                    'maintenance': 80
                },
                'python': {
                    'description': 'Python 是一种广泛使用的高级编程语言',
                    'pros': ['简洁易读', '丰富的库', '强大的数据科学生态', '快速开发'],
                    'cons': ['性能相对较低', 'GIL 限制并发', '部署相对复杂'],
                    'use_cases': ['数据科学', '机器学习', '后端 API', '脚本工具'],
                    'popularity': 95,
                    'community': 90,
                    'maintenance': 85
                },
                'java': {
                    'description': 'Java 是一种广泛使用的计算机编程语言',
                    'pros': ['跨平台', '强类型', '成熟的生态', '企业级支持'],
                    'cons': ['语法 verbose', '启动时间长', '内存占用大'],
                    'use_cases': ['企业应用', '大型系统', 'Android 开发', '微服务'],
                    'popularity': 85,
                    'community': 80,
                    'maintenance': 90
                },
                'go': {
                    'description': 'Go 是 Google 开发的开源编程语言',
                    'pros': ['高性能', '简洁语法', '内置并发', '快速编译'],
                    'cons': ['生态系统相对年轻', '错误处理 verbose', '泛型支持有限'],
                    'use_cases': ['高并发服务', '微服务', '系统编程', '云原生应用'],
                    'popularity': 80,
                    'community': 75,
                    'maintenance': 85
                }
            },
            'database': {
                'mongodb': {
                    'description': 'MongoDB 是一个基于文档的 NoSQL 数据库',
                    'pros': ['灵活的文档模型', '水平扩展', '快速开发', '适合非结构化数据'],
                    'cons': ['查询性能有限', '占用空间大', '事务支持有限'],
                    'use_cases': ['内容管理系统', '移动应用后端', '实时分析', '物联网数据'],
                    'popularity': 85,
                    'community': 80,
                    'maintenance': 80
                },
                'postgresql': {
                    'description': 'PostgreSQL 是一个功能强大的开源关系型数据库',
                    'pros': ['强大的 SQL 支持', '可靠性高', '高级特性丰富', '扩展性好'],
                    'cons': ['配置复杂', '性能调优需要专业知识', '资源消耗较大'],
                    'use_cases': ['企业应用', '数据仓库', '需要复杂查询的场景', '金融系统'],
                    'popularity': 80,
                    'community': 75,
                    'maintenance': 85
                },
                'mysql': {
                    'description': 'MySQL 是一个流行的关系型数据库管理系统',
                    'pros': ['易于使用', '性能稳定', '社区支持广泛', '适合 web 应用'],
                    'cons': ['高级特性相对较少', '扩展性有限', '开源版本功能受限'],
                    'use_cases': ['Web 应用', '内容管理系统', '电子商务', '小型企业应用'],
                    'popularity': 90,
                    'community': 85,
                    'maintenance': 80
                },
                'redis': {
                    'description': 'Redis 是一个开源的内存数据结构存储',
                    'pros': ['极高的性能', '丰富的数据结构', '支持持久化', '适合缓存'],
                    'cons': ['内存消耗大', '数据量受内存限制', '复杂查询支持有限'],
                    'use_cases': ['缓存', '会话存储', '实时分析', '消息队列'],
                    'popularity': 85,
                    'community': 80,
                    'maintenance': 80
                }
            }
        }
        
        self.project_types = {
            'ecommerce': {
                'frontend': ['react', 'vue'],
                'backend': ['nodejs', 'python'],
                'database': ['postgresql', 'mongodb']
            },
            'saas': {
                'frontend': ['react', 'angular'],
                'backend': ['nodejs', 'python', 'go'],
                'database': ['postgresql', 'mongodb']
            },
            'mobile_app': {
                'frontend': ['react', 'vue'],
                'backend': ['nodejs', 'python', 'go'],
                'database': ['mongodb', 'postgresql']
            },
            'content_management': {
                'frontend': ['react', 'vue'],
                'backend': ['nodejs', 'python'],
                'database': ['mongodb', 'mysql']
            },
            'data_science': {
                'frontend': ['react', 'vue'],
                'backend': ['python'],
                'database': ['postgresql', 'mongodb']
            }
        }
    
    def analyze_project(self, project_description, constraints=None):
        """分析项目需求
        
        Args:
            project_description: 项目描述
            constraints: 约束条件
            
        Returns:
            analysis: 分析结果
        """
        analysis = {
            'project_type': self._detect_project_type(project_description),
            'requirements': self._extract_requirements(project_description),
            'constraints': constraints or {}
        }
        return analysis
    
    def _detect_project_type(self, project_description):
        """检测项目类型
        
        Args:
            project_description: 项目描述
            
        Returns:
            project_type: 项目类型
        """
        description_lower = project_description.lower()
        
        if any(keyword in description_lower for keyword in ['电商', '购物', 'ecommerce', 'shop', 'store']):
            return 'ecommerce'
        elif any(keyword in description_lower for keyword in ['saas', '软件即服务', '企业服务']):
            return 'saas'
        elif any(keyword in description_lower for keyword in ['移动', 'app', 'mobile']):
            return 'mobile_app'
        elif any(keyword in description_lower for keyword in ['内容', 'cms', 'content', '管理系统']):
            return 'content_management'
        elif any(keyword in description_lower for keyword in ['数据', '分析', 'data', 'science', 'ml', 'ai']):
            return 'data_science'
        else:
            return 'general'
    
    def _extract_requirements(self, project_description):
        """提取项目需求
        
        Args:
            project_description: 项目描述
            
        Returns:
            requirements: 需求列表
        """
        requirements = []
        
        # 性能需求
        if any(keyword in project_description.lower() for keyword in ['性能', '快速', 'high performance', 'fast']):
            requirements.append('performance')
        
        # 可扩展性需求
        if any(keyword in project_description.lower() for keyword in ['扩展', 'scale', 'scalable']):
            requirements.append('scalability')
        
        # 安全性需求
        if any(keyword in project_description.lower() for keyword in ['安全', 'security', 'secure']):
            requirements.append('security')
        
        # 实时性需求
        if any(keyword in project_description.lower() for keyword in ['实时', 'real-time', 'realtime']):
            requirements.append('realtime')
        
        # 数据密集型需求
        if any(keyword in project_description.lower() for keyword in ['数据', 'data', 'database']):
            requirements.append('data_intensive')
        
        return requirements
    
    def recommend(self, project_description, constraints=None):
        """推荐技术栈
        
        Args:
            project_description: 项目描述
            constraints: 约束条件
            
        Returns:
            recommendation: 推荐结果
        """
        # 分析项目
        analysis = self.analyze_project(project_description, constraints)
        
        # 生成推荐
        recommendation = {
            'analysis': analysis,
            'recommendations': {
                'frontend': self._recommend_frontend(analysis),
                'backend': self._recommend_backend(analysis),
                'database': self._recommend_database(analysis)
            },
            'justification': self._generate_justification(analysis),
            'timestamp': datetime.now().isoformat()
        }
        
        return recommendation
    
    def _recommend_frontend(self, analysis):
        """推荐前端技术栈
        
        Args:
            analysis: 项目分析结果
            
        Returns:
            frontend_recommendations: 前端推荐列表
        """
        project_type = analysis['project_type']
        requirements = analysis['requirements']
        constraints = analysis['constraints']
        
        # 获取适合该项目类型的前端技术
        suitable_techs = self.project_types.get(project_type, {}).get('frontend', list(self.tech_stack_data['frontend'].keys()))
        
        # 过滤约束条件
        if 'frontend' in constraints:
            suitable_techs = [tech for tech in suitable_techs if tech in constraints['frontend']]
        
        # 排序技术栈
        ranked_techs = []
        for tech in suitable_techs:
            score = self._calculate_score('frontend', tech, requirements)
            ranked_techs.append((tech, score))
        
        # 按分数排序
        ranked_techs.sort(key=lambda x: x[1], reverse=True)
        
        # 生成推荐列表
        recommendations = []
        for tech, score in ranked_techs:
            tech_data = self.tech_stack_data['frontend'][tech]
            recommendations.append({
                'tech': tech,
                'score': score,
                'description': tech_data['description'],
                'pros': tech_data['pros'],
                'cons': tech_data['cons']
            })
        
        return recommendations
    
    def _recommend_backend(self, analysis):
        """推荐后端技术栈
        
        Args:
            analysis: 项目分析结果
            
        Returns:
            backend_recommendations: 后端推荐列表
        """
        project_type = analysis['project_type']
        requirements = analysis['requirements']
        constraints = analysis['constraints']
        
        # 获取适合该项目类型的后端技术
        suitable_techs = self.project_types.get(project_type, {}).get('backend', list(self.tech_stack_data['backend'].keys()))
        
        # 过滤约束条件
        if 'backend' in constraints:
            suitable_techs = [tech for tech in suitable_techs if tech in constraints['backend']]
        
        # 排序技术栈
        ranked_techs = []
        for tech in suitable_techs:
            score = self._calculate_score('backend', tech, requirements)
            ranked_techs.append((tech, score))
        
        # 按分数排序
        ranked_techs.sort(key=lambda x: x[1], reverse=True)
        
        # 生成推荐列表
        recommendations = []
        for tech, score in ranked_techs:
            tech_data = self.tech_stack_data['backend'][tech]
            recommendations.append({
                'tech': tech,
                'score': score,
                'description': tech_data['description'],
                'pros': tech_data['pros'],
                'cons': tech_data['cons']
            })
        
        return recommendations
    
    def _recommend_database(self, analysis):
        """推荐数据库技术栈
        
        Args:
            analysis: 项目分析结果
            
        Returns:
            database_recommendations: 数据库推荐列表
        """
        project_type = analysis['project_type']
        requirements = analysis['requirements']
        constraints = analysis['constraints']
        
        # 获取适合该项目类型的数据库技术
        suitable_techs = self.project_types.get(project_type, {}).get('database', list(self.tech_stack_data['database'].keys()))
        
        # 过滤约束条件
        if 'database' in constraints:
            suitable_techs = [tech for tech in suitable_techs if tech in constraints['database']]
        
        # 排序技术栈
        ranked_techs = []
        for tech in suitable_techs:
            score = self._calculate_score('database', tech, requirements)
            ranked_techs.append((tech, score))
        
        # 按分数排序
        ranked_techs.sort(key=lambda x: x[1], reverse=True)
        
        # 生成推荐列表
        recommendations = []
        for tech, score in ranked_techs:
            tech_data = self.tech_stack_data['database'][tech]
            recommendations.append({
                'tech': tech,
                'score': score,
                'description': tech_data['description'],
                'pros': tech_data['pros'],
                'cons': tech_data['cons']
            })
        
        return recommendations
    
    def _calculate_score(self, category, tech, requirements):
        """计算技术栈得分
        
        Args:
            category: 技术类别
            tech: 技术名称
            requirements: 项目需求
            
        Returns:
            score: 得分
        """
        tech_data = self.tech_stack_data[category][tech]
        
        # 基础得分
        score = (
            tech_data['popularity'] * 0.3 +
            tech_data['community'] * 0.3 +
            tech_data['maintenance'] * 0.4
        )
        
        # 根据需求调整得分
        if 'performance' in requirements:
            if category == 'frontend' and tech in ['svelte', 'react']:
                score += 10
            elif category == 'backend' and tech in ['go', 'nodejs']:
                score += 10
            elif category == 'database' and tech in ['redis', 'mongodb']:
                score += 10
        
        if 'scalability' in requirements:
            if category == 'backend' and tech in ['go', 'nodejs']:
                score += 10
            elif category == 'database' and tech in ['mongodb', 'postgresql']:
                score += 10
        
        if 'security' in requirements:
            if category == 'backend' and tech in ['java', 'go']:
                score += 10
            elif category == 'database' and tech in ['postgresql', 'mysql']:
                score += 10
        
        if 'realtime' in requirements:
            if category == 'backend' and tech in ['nodejs', 'go']:
                score += 10
            elif category == 'database' and tech in ['redis', 'mongodb']:
                score += 10
        
        if 'data_intensive' in requirements:
            if category == 'backend' and tech in ['python', 'java']:
                score += 10
            elif category == 'database' and tech in ['postgresql', 'mongodb']:
                score += 10
        
        return min(100, score)
    
    def _generate_justification(self, analysis):
        """生成推荐理由
        
        Args:
            analysis: 项目分析结果
            
        Returns:
            justification: 推荐理由
        """
        project_type = analysis['project_type']
        requirements = analysis['requirements']
        
        justifications = []
        
        # 项目类型理由
        project_type_justifications = {
            'ecommerce': '这是一个电商项目，需要稳定的前端体验和可靠的后端处理能力。',
            'saas': '这是一个SaaS项目，需要可扩展的架构和企业级的可靠性。',
            'mobile_app': '这是一个移动应用项目，需要高效的API和灵活的数据存储。',
            'content_management': '这是一个内容管理系统，需要灵活的内容结构和快速的前端渲染。',
            'data_science': '这是一个数据科学项目，需要强大的数据处理能力和可视化支持。',
            'general': '这是一个通用项目，推荐使用广泛采用的技术栈。'
        }
        
        justifications.append(project_type_justifications.get(project_type, project_type_justifications['general']))
        
        # 需求理由
        if 'performance' in requirements:
            justifications.append('项目对性能要求较高，推荐使用高性能的技术栈。')
        if 'scalability' in requirements:
            justifications.append('项目需要良好的可扩展性，推荐使用支持水平扩展的技术栈。')
        if 'security' in requirements:
            justifications.append('项目对安全性要求较高，推荐使用安全性好的技术栈。')
        if 'realtime' in requirements:
            justifications.append('项目需要实时功能，推荐使用支持实时通信的技术栈。')
        if 'data_intensive' in requirements:
            justifications.append('项目是数据密集型的，推荐使用适合处理大量数据的技术栈。')
        
        return ' '.join(justifications)
    
    def save_recommendation(self, recommendation, file_path):
        """保存推荐结果
        
        Args:
            recommendation: 推荐结果
            file_path: 保存路径
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(recommendation, f, ensure_ascii=False, indent=2)
            print(f"推荐结果保存成功: {file_path}")
        except Exception as e:
            print(f"保存推荐结果失败: {str(e)}")
    
    def load_recommendation(self, file_path):
        """加载推荐结果
        
        Args:
            file_path: 文件路径
            
        Returns:
            recommendation: 推荐结果
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                recommendation = json.load(f)
            return recommendation
        except Exception as e:
            print(f"加载推荐结果失败: {str(e)}")
            return None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python tech_stack_recommender.py <项目描述> [约束条件JSON]")
        print('示例: python tech_stack_recommender.py "一个电商平台，需要高性能和可扩展性" "{\"frontend\": [\"react\", \"vue\"]}"')
        sys.exit(1)
    
    project_description = sys.argv[1]
    constraints = None
    
    if len(sys.argv) > 2:
        try:
            constraints = json.loads(sys.argv[2])
        except Exception as e:
            print(f"约束条件解析失败: {str(e)}")
            sys.exit(1)
    
    recommender = TechStackRecommender()
    recommendation = recommender.recommend(project_description, constraints)
    
    # 打印推荐结果
    print("\n=== 技术栈推荐结果 ===")
    print(f"项目类型: {recommendation['analysis']['project_type']}")
    print(f"需求: {', '.join(recommendation['analysis']['requirements'])}")
    print(f"推荐理由: {recommendation['justification']}")
    
    print("\n--- 前端推荐 ---")
    for rec in recommendation['recommendations']['frontend'][:3]:
        print(f"{rec['tech']} (得分: {rec['score']:.1f})")
        print(f"  描述: {rec['description']}")
        print(f"  优点: {', '.join(rec['pros'])}")
        print(f"  缺点: {', '.join(rec['cons'])}")
        print()
    
    print("--- 后端推荐 ---")
    for rec in recommendation['recommendations']['backend'][:3]:
        print(f"{rec['tech']} (得分: {rec['score']:.1f})")
        print(f"  描述: {rec['description']}")
        print(f"  优点: {', '.join(rec['pros'])}")
        print(f"  缺点: {', '.join(rec['cons'])}")
        print()
    
    print("--- 数据库推荐 ---")
    for rec in recommendation['recommendations']['database'][:3]:
        print(f"{rec['tech']} (得分: {rec['score']:.1f})")
        print(f"  描述: {rec['description']}")
        print(f"  优点: {', '.join(rec['pros'])}")
        print(f"  缺点: {', '.join(rec['cons'])}")
        print()
    
    # 保存推荐结果
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"tech_stack_recommendation_{timestamp}.json"
    recommender.save_recommendation(recommendation, output_file)
    print(f"推荐结果已保存到: {output_file}")

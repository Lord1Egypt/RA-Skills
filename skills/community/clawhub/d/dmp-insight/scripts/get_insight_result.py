#!/usr/bin/env python3
"""
获取人群洞察任务结果（增强版）
功能：获取洞察数据并自动生成Excel表格
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path

def find_auth_skill_path():
    """
    动态查找鉴权技能的API脚本路径
    
    Returns:
        Path: 鉴权技能的minri_dmp_api.py路径，如果未找到则返回None
    """
    # 第一层：固定路径列表（按优先级排序）
    possible_paths = [
        # 标准安装路径
        Path.home() / ".skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        # OpenClaw workspace路径
        Path.home() / ".openclaw" / "workspace" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        # OpenClaw skills路径
        Path.home() / ".openclaw" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        # workspace中的路径（skill_id 8863）
        Path.cwd() / ".skills" / "8863" / "scripts" / "minri_dmp_api.py",
        # workspace中的路径（按名称）
        Path.cwd() / ".skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
    ]
    
    # 检查固定路径
    for path in possible_paths:
        if path.exists():
            return path
    
    # 第二层：动态扫描所有可能的目录
    scan_dirs = [
        Path.home() / ".skills",
        Path.home() / ".openclaw" / "workspace" / "skills",
        Path.home() / ".openclaw" / "skills",
        Path.cwd() / ".skills",
    ]
    for scan_dir in scan_dirs:
        if scan_dir.exists():
            for skill_dir in scan_dir.iterdir():
                if skill_dir.is_dir():
                    auth_path = skill_dir / "scripts" / "minri_dmp_api.py"
                    if auth_path.exists():
                        try:
                            with open(auth_path, 'r', encoding='utf-8') as f:
                                content = f.read(500)
                                if "明日DMP" in content or "mingdata" in content.lower():
                                    return auth_path
                        except:
                            continue
    
    return None

def flatten_insight_data(data_list, level1='', level2='', level3='', level4=''):
    """将树形结构的洞察数据展平为表格格式"""
    rows = []
    
    for item in data_list:
        # 当前节点信息
        current_name = item.get('name', '')
        
        # 确定当前层级
        if not level1:
            current_level1 = current_name
            current_level2 = ''
            current_level3 = ''
            current_level4 = ''
        elif not level2:
            current_level1 = level1
            current_level2 = current_name
            current_level3 = ''
            current_level4 = ''
        elif not level3:
            current_level1 = level1
            current_level2 = level2
            current_level3 = current_name
            current_level4 = ''
        elif not level4:
            current_level1 = level1
            current_level2 = level2
            current_level3 = level3
            current_level4 = current_name
        else:
            current_level1 = level1
            current_level2 = level2
            current_level3 = level3
            current_level4 = level4
        
        row = {
            '一级分类': current_level1,
            '二级分类': current_level2,
            '三级分类': current_level3,
            '四级分类': current_level4,
            '维度名称': current_name,
            '覆盖率': item.get('coverageRate', 0),
            'TGI指数': item.get('tgi', 0),
            '维度类型': '分类' if item.get('type') == 0 else '标签',
            '维度ID': item.get('id', ''),
            '父级ID': item.get('parentId', ''),
            '父级名称': item.get('parentName', '')
        }
        
        rows.append(row)
        
        # 递归处理子节点
        if 'children' in item and item['children']:
            child_rows = flatten_insight_data(
                item['children'], 
                current_level1, 
                current_level2, 
                current_level3, 
                current_level4
            )
            rows.extend(child_rows)
    
    return rows

def generate_excel(task_id, api_data):
    """
    生成Excel表格文件（强制执行，确保数据一致性）
    
    Returns:
        dict: 包含生成结果的字典
    """
    try:
        import pandas as pd
        from datetime import datetime
        
        # 数据完整性检查
        if not api_data or 'data' not in api_data:
            raise ValueError("API数据为空或格式错误")
        
        insight_data = api_data.get('data', [])
        if not insight_data:
            raise ValueError("洞察数据为空")
        
        # 展平数据
        flattened_data = flatten_insight_data(insight_data)
        
        if not flattened_data:
            raise ValueError("数据展平失败，未获取到任何记录")
        
        # 创建DataFrame
        df = pd.DataFrame(flattened_data)
        
        # 数据验证：确保必要字段存在
        required_columns = ['一级分类', '二级分类', '三级分类', '四级分类', '维度名称', '覆盖率', 'TGI指数']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"缺少必要字段: {', '.join(missing_columns)}")
        
        # 格式化数值（确保数据类型正确）
        df['覆盖率_数值'] = pd.to_numeric(df['覆盖率'], errors='coerce').fillna(0)
        df['覆盖率'] = df['覆盖率_数值'].apply(lambda x: f"{x*100:.2f}%" if x > 0 else "0.00%")
        df['TGI指数_数值'] = pd.to_numeric(df['TGI指数'], errors='coerce').fillna(0)
        df['TGI指数'] = df['TGI指数_数值'].apply(lambda x: f"{x:.2f}" if x > 0 else "0.00")
        
        # 调整列顺序（确保每次输出格式一致）
        columns_order = ['一级分类', '二级分类', '三级分类', '四级分类', '维度名称', '覆盖率', 'TGI指数', 
                         '维度类型', '维度ID', '父级ID', '父级名称', '覆盖率_数值', 'TGI指数_数值']
        df = df[columns_order]
        
        # 创建Excel文件，包含多个工作表
        excel_file = f"洞察任务{task_id}_完整数据表格.xlsx"
        
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            # 工作表1: 完整数据（按一级分类、TGI指数排序，确保每次顺序一致）
            df_sorted = df.sort_values(['一级分类', 'TGI指数_数值'], ascending=[True, False])
            df_sorted.to_excel(writer, sheet_name='完整洞察数据', index=False)
            
            # 工作表2: 高TGI特征（TGI > 200，按TGI降序）
            high_tgi = df[df['TGI指数_数值'] > 200].sort_values('TGI指数_数值', ascending=False)
            high_tgi.to_excel(writer, sheet_name='高TGI特征(>200)', index=False)
            
            # 工作表3: 按一级分类汇总
            if len(df[df['一级分类'] != '']) > 0:
                summary_by_level1 = df[df['一级分类'] != ''].groupby('一级分类').agg({
                    '覆盖率_数值': 'max',
                    'TGI指数_数值': 'max',
                    '维度ID': 'count'
                }).reset_index()
                summary_by_level1.columns = ['一级分类', '最大覆盖率', '最大TGI指数', '维度数量']
                summary_by_level1['最大覆盖率'] = summary_by_level1['最大覆盖率'].apply(lambda x: f"{x*100:.2f}%")
                summary_by_level1['最大TGI指数'] = summary_by_level1['最大TGI指数'].apply(lambda x: f"{x:.2f}")
                summary_by_level1 = summary_by_level1.sort_values('一级分类')  # 按分类名称排序
                summary_by_level1.to_excel(writer, sheet_name='一级分类汇总', index=False)
            else:
                # 如果没有分类数据，创建空工作表
                pd.DataFrame(columns=['一级分类', '最大覆盖率', '最大TGI指数', '维度数量']).to_excel(
                    writer, sheet_name='一级分类汇总', index=False
                )
        
        # 验证文件是否成功生成
        if not Path(excel_file).exists():
            raise FileNotFoundError(f"Excel文件生成失败: {excel_file}")
        
        # 返回详细的生成结果
        return {
            "success": True,
            "excel_file": excel_file,
            "total_records": len(df),
            "high_tgi_count": len(high_tgi),
            "categories_count": len(df[df['一级分类'] != ''].groupby('一级分类')) if len(df[df['一级分类'] != '']) > 0 else 0,
            "generation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_integrity": "verified"
        }
        
    except ImportError as e:
        # pandas未安装，这是严重错误
        return {
            "success": False,
            "error": "PANDAS_NOT_FOUND",
            "message": f"pandas库未安装，无法生成Excel文件: {str(e)}",
            "suggestion": "请安装pandas和openpyxl库: pip install pandas openpyxl"
        }
    except Exception as e:
        # 其他错误
        import traceback
        return {
            "success": False,
            "error": "EXCEL_GENERATION_FAILED",
            "message": f"Excel生成失败: {str(e)}",
            "traceback": traceback.format_exc()
        }

def call_api(task_id):
    """
    调用鉴权技能获取洞察任务结果
    
    Args:
        task_id: 任务ID
    """
    # 动态查找鉴权技能的API脚本路径
    auth_skill_path = find_auth_skill_path()
    
    if not auth_skill_path:
        print(json.dumps({
            "error": "AUTH_SKILL_NOT_FOUND",
            "message": "未找到鉴权技能，请先安装mingdata-dmp-auth技能"
        }, ensure_ascii=False))
        sys.exit(3)
    
    # 调用鉴权技能的API脚本（正确的endpoint路径，不包含/api/open-api前缀）
    try:
        result = subprocess.run(
            [
                "python3", 
                str(auth_skill_path), 
                "GET", 
                "/audience/insight/result",
                json.dumps({"taskId": int(task_id)})
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # 解析API返回结果
        try:
            api_data = json.loads(result.stdout)
            
            # 如果API调用成功，强制生成Excel和JSON
            if result.returncode == 0 and api_data.get('code') == '0':
                # 保存JSON数据
                json_file = f"洞察任务{task_id}_API原始数据.json"
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(api_data, f, ensure_ascii=False, indent=2)
                
                # 生成Excel（强制执行）
                excel_result = generate_excel(task_id, api_data)
                
                # 检查Excel是否成功生成
                if excel_result.get('success'):
                    # Excel生成成功
                    output = {
                        "success": True,
                        "task_id": task_id,
                        "files_generated": {
                            "json": json_file,
                            "excel": excel_result.get('excel_file')
                        },
                        "data_summary": {
                            "total_records": excel_result.get('total_records'),
                            "high_tgi_count": excel_result.get('high_tgi_count'),
                            "categories_count": excel_result.get('categories_count'),
                            "generation_time": excel_result.get('generation_time'),
                            "data_integrity": excel_result.get('data_integrity')
                        },
                        "message": "✅ 洞察数据获取成功，已自动生成Excel表格和JSON数据文件"
                    }
                    print(json.dumps(output, ensure_ascii=False, indent=2))
                else:
                    # Excel生成失败，但JSON已保存
                    output = {
                        "success": False,
                        "task_id": task_id,
                        "files_generated": {
                            "json": json_file,
                            "excel": None
                        },
                        "excel_error": {
                            "error": excel_result.get('error'),
                            "message": excel_result.get('message'),
                            "suggestion": excel_result.get('suggestion', '请检查pandas和openpyxl库是否已安装')
                        },
                        "message": "⚠️ 洞察数据获取成功，但Excel生成失败，仅保存了JSON数据"
                    }
                    print(json.dumps(output, ensure_ascii=False, indent=2))
                    sys.exit(5)  # Excel生成失败的退出码
            else:
                # API调用失败，直接输出原始结果
                print(result.stdout)
        except json.JSONDecodeError:
            # 无法解析JSON，直接输出原始结果
            print(result.stdout)
        
        # 传递退出码
        sys.exit(result.returncode)
        
    except subprocess.TimeoutExpired:
        print(json.dumps({
            "error": "TIMEOUT",
            "message": "API调用超时"
        }, ensure_ascii=False))
        sys.exit(6)
    except Exception as e:
        print(json.dumps({
            "error": "CALL_ERROR",
            "message": f"调用鉴权技能失败: {str(e)}"
        }, ensure_ascii=False))
        sys.exit(6)

def main():
    parser = argparse.ArgumentParser(description='获取人群洞察任务结果并生成Excel表格')
    parser.add_argument('task_id', help='洞察任务ID')
    
    args = parser.parse_args()
    
    # 调用API
    call_api(args.task_id)

if __name__ == "__main__":
    main()

import requests
import json

# 配置参数
config = {
    "host": "http://agent-data.ihdwork.com",
    "base_path": "/handi-ai",
    "endpoint": "/ent-analysis/main-business"
}

def get_ent_main_business(ent_id):
    """企业主营业务检索
    
    Args:
        ent_id (int): 企业ID（必须）
        
    Returns:
        dict: 包含企业主营业务信息的字典
    """
    # 构建完整URL
    url = f"{config['host']}{config['base_path']}{config['endpoint']}"
    
    # 构建请求头
    headers = {
        "Content-Type": "application/json"
    }
    
    # 构建请求体
    payload = {
        "ent_id": ent_id
    }
    
    try:
        print(f"=== 查询企业主营业务 (企业ID: {ent_id}) ===")
        print(f"URL: {url}")
        print(f"请求头: {headers}")
        print(f"请求体: {json.dumps(payload, ensure_ascii=False)}")
        
        # 发送POST请求
        response = requests.post(
            url=url,
            headers=headers,
            data=json.dumps(payload),
            timeout=10
        )
        
        print(f"\n状态码: {response.status_code}")
        print(f"响应文本: {response.text}")
        
        # 尝试解析JSON
        try:
            result = response.json()
            print("\n解析后的JSON响应:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
            # 处理返回的数据
            if isinstance(result, dict):
                return {
                    'data': result,
                    'success': True
                }
            else:
                return {
                    'raw_data': result,
                    'success': True
                }
                
        except json.JSONDecodeError:
            print("响应不是JSON格式")
            return {
                'raw_text': response.text,
                'success': False
            }
            
    except Exception as e:
        print(f"请求失败: {str(e)}")
        return {
            'error': str(e),
            'success': False
        }

def print_main_business(result):
    """格式化打印企业主营业务信息"""
    if not result.get('success'):
        print("请求未成功")
        return
    
    data = result.get('data')
    if not data:
        print("未获取到企业主营业务数据")
        return
    
    # 尝试多种数据提取方式
    business_data = data.get('data', {}) or data
    
    print("\n" + "="*50)
    print("企业主营业务")
    print("="*50)
    print(f"主营产品: {business_data.get('main_product', 'N/A')}")
    print(f"主营业务: {business_data.get('main_biz', 'N/A')}")

if __name__ == "__main__":
    # 示例调用：查询企业主营业务
    test_ent_id = "toygPBcZl33"  # 企业ID（字符串格式）
    
    # 查询企业主营业务
    result = get_ent_main_business(test_ent_id)
    
    # 打印格式化的主营业务信息
    if result.get('success'):
        print_main_business(result)
    else:
        print("\n❌ 查询失败")
        if 'error' in result:
            print(f"错误信息: {result['error']}")
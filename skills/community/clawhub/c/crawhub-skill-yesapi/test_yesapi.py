#!/usr/bin/env python3
"""
YesApi 完整接口测试脚本
测试所有 API 接口的功能
"""

import os
import json
import time
from dotenv import load_dotenv
from yesapi_client import YesApiClient, YesApiError, YesApiConfig

# 加载环境变量
load_dotenv()

class YesApiComprehensiveTest:
    def __init__(self):
        self.client = None
        self.test_model_name = f"test_model_{int(time.time())}"
        self.test_record_id = None
        self.init_client()
    
    def init_client(self):
        """初始化客户端"""
        try:
            config = YesApiConfig(
                app_key=os.getenv("YESAPI_APP_KEY", ""),
                domain=os.getenv("YESAPI_DOMAIN", "https://api.yesapi.net"),
                sign=os.getenv("YESAPI_SIGN", "")
            )
            self.client = YesApiClient(config)
            print("✅ 客户端初始化成功")
        except Exception as e:
            print(f"❌ 客户端初始化失败: {e}")
            exit(1)
    
    def test_get_models(self):
        """测试获取模型列表"""
        print("\n=== 测试获取模型列表 ===")
        try:
            result = self.client.get_models()
            print("✅ 获取模型列表成功")
            print(f"返回数据: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return result
        except YesApiError as e:
            print(f"❌ 获取模型列表失败: {e}, ret: {e.ret}")
            return None
        except Exception as e:
            print(f"❌ 未知错误: {e}")
            return None
    
    def test_create_model(self):
        """测试创建模型"""
        print(f"\n=== 测试创建模型: {self.test_model_name} ===")
        try:
            result = self.client.create_model(
                model_name=self.test_model_name,
                model_desc="测试模型描述"
            )
            print("✅ 创建模型成功")
            print(f"返回数据: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return result
        except YesApiError as e:
            print(f"❌ 创建模型失败: {e}, ret: {e.ret}")
            return None
        except Exception as e:
            print(f"❌ 未知错误: {e}")
            return None
    
    def test_add_field(self):
        """测试添加字段"""
        print(f"\n=== 测试添加字段到模型: {self.test_model_name} ===")
        try:
            # 添加不同类型的字段
            fields_to_add = [
                ("username", "姓名", "varchar", 50),
                ("age", "年龄", "int", 0),
                ("email", "邮箱", "varchar", 100),
                ("created_at", "创建时间", "datetime", 0)
            ]
            
            for field_name, field_desc, field_type, field_length in fields_to_add:
                result = self.client.add_model_new_field(
                    model_name=self.test_model_name,
                    field_name=field_name,
                    field_desc=field_desc,
                    field_type=field_type,
                    field_length=field_length
                )
                print(f"✅ 添加字段 {field_name} 成功")
                print(f"返回数据: {json.dumps(result, indent=2, ensure_ascii=False)}")
                time.sleep(1)  # 避免请求过快
            
            return True
        except YesApiError as e:
            print(f"❌ 添加字段失败: {e}, ret: {e.ret}")
            return False
        except Exception as e:
            print(f"❌ 未知错误: {e}")
            return False
    
    def test_insert_data(self):
        """测试插入数据"""
        print(f"\n=== 测试插入数据到模型: {self.test_model_name} ===")
        try:
            test_data = {
                "username": "张三",
                "age": 25,
                "email": "zhangsan@example.com",
                "created_at": "2026-01-01 00:00:00"
            }
            
            result = self.client.insert_data(
                model_name=self.test_model_name,
                data=test_data
            )
            print("✅ 插入数据成功")
            print(f"返回数据: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 保存记录ID用于后续测试
            if result and 'id' in result:
                self.test_record_id = result['id']
                print(f"保存记录ID: {self.test_record_id}")
            
            return result
        except YesApiError as e:
            print(f"❌ 插入数据失败: {e}, ret: {e.ret}")
            return None
        except Exception as e:
            print(f"❌ 未知错误: {e}")
            return None
    
    def test_query_data(self):
        """测试查询数据"""
        print(f"\n=== 测试查询数据: {self.test_model_name} ===")
        try:
            # 基本查询
            result = self.client.query_data(
                model_name=self.test_model_name,
                page=1,
                perpage=10
            )
            print("✅ 查询数据成功")
            print(f"返回数据: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 带条件的查询
            print("\n--- 测试带条件的查询 ---")
            result_with_where = self.client.query_data(
                model_name=self.test_model_name,
                page=1,
                perpage=5,
                where=json.dumps([["username", "=", "张三"]])
            )
            print("✅ 带条件查询成功")
            print(f"返回数据: {json.dumps(result_with_where, indent=2, ensure_ascii=False)}")
            
            return result
        except YesApiError as e:
            print(f"❌ 查询数据失败: {e}, ret: {e.ret}")
            return None
        except Exception as e:
            print(f"❌ 未知错误: {e}")
            return None
    
    def test_update_data(self):
        """测试更新数据"""
        if not self.test_record_id:
            print("❌ 没有可用的记录ID进行更新测试")
            return None
            
        print(f"\n=== 测试更新数据: {self.test_model_name}, ID: {self.test_record_id} ===")
        try:
            update_data = {
                "username": "李四",
                "age": 30
            }
            
            result = self.client.update_data(
                model_name=self.test_model_name,
                record_id=self.test_record_id,
                data=update_data
            )
            print("✅ 更新数据成功")
            print(f"返回数据: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return result
        except YesApiError as e:
            print(f"❌ 更新数据失败: {e}, ret: {e.ret}")
            return None
        except Exception as e:
            print(f"❌ 未知错误: {e}")
            return None
    
    def test_batch_update(self):
        """测试批量更新"""
        print(f"\n=== 测试批量更新: {self.test_model_name} ===")
        try:
            where_condition = [["age", "=", 25]]
            update_data = {"age": 26}
            
            result = self.client.batch_update(
                model_name=self.test_model_name,
                where=where_condition,
                data=update_data
            )
            print("✅ 批量更新成功")
            print(f"返回数据: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return result
        except YesApiError as e:
            print(f"❌ 批量更新失败: {e}, ret: {e.ret}")
            return None
        except Exception as e:
            print(f"❌ 未知错误: {e}")
            return None
    
    def test_delete_data(self):
        """测试删除数据"""
        if not self.test_record_id:
            print("❌ 没有可用的记录ID进行删除测试")
            return None
            
        print(f"\n=== 测试删除数据: {self.test_model_name}, ID: {self.test_record_id} ===")
        try:
            result = self.client.delete_data(
                model_name=self.test_model_name,
                record_id=self.test_record_id
            )
            print("✅ 删除数据成功")
            print(f"返回数据: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return result
        except YesApiError as e:
            print(f"❌ 删除数据失败: {e}, ret: {e.ret}")
            return None
        except Exception as e:
            print(f"❌ 未知错误: {e}")
            return None
    
    def test_batch_delete(self):
        """测试批量删除"""
        print(f"\n=== 测试批量删除: {self.test_model_name} ===")
        try:
            # 先插入一些测试数据
            test_data1 = {"username": "测试用户", "age": 25}
            test_data2 = {"username": "测试用户", "age": 26}
            
            self.client.insert_data(self.test_model_name, test_data1)
            self.client.insert_data(self.test_model_name, test_data2)
            time.sleep(1)
            
            # 批量删除
            where_condition = [["username", "=", "测试用户"]]
            result = self.client.batch_delete(
                model_name=self.test_model_name,
                where=where_condition
            )
            print("✅ 批量删除成功")
            print(f"返回数据: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return result
        except YesApiError as e:
            print(f"❌ 批量删除失败: {e}, ret: {e.ret}")
            return None
        except Exception as e:
            print(f"❌ 未知错误: {e}")
            return None
    
    def test_delete_model(self):
        """测试删除模型"""
        print(f"\n=== 测试删除模型: {self.test_model_name} ===")
        try:
            result = self.client.delete_model(
                model_name=self.test_model_name,
                is_drop_table=True
            )
            print("✅ 删除模型成功")
            print(f"返回数据: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return result
        except YesApiError as e:
            print(f"❌ 删除模型失败: {e}, ret: {e.ret}")
            return None
        except Exception as e:
            print(f"❌ 未知错误: {e}")
            return None
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 60)
        print("YesApi 完整接口测试开始")
        print("=" * 60)
        
        # 测试顺序：创建 -> 操作 -> 删除
        test_sequence = [
            ("获取模型列表", self.test_get_models),
            ("创建模型", self.test_create_model),
            ("添加字段", self.test_add_field),
            ("插入数据", self.test_insert_data),
            ("查询数据", self.test_query_data),
            ("更新数据", self.test_update_data),
            ("批量更新", self.test_batch_update),
            ("删除数据", self.test_delete_data),
            ("批量删除", self.test_batch_delete),
            # ("删除模型", self.test_delete_model),
        ]
        
        results = {}
        
        for test_name, test_func in test_sequence:
            try:
                result = test_func()
                results[test_name] = "✅ 成功" if result else "❌ 失败"
                time.sleep(0.5)  # 避免请求过快
            except Exception as e:
                results[test_name] = f"❌ 异常: {str(e)}"
        
        # 打印测试总结
        print("\n" + "=" * 60)
        print("测试结果总结")
        print("=" * 60)
        
        for test_name, status in results.items():
            print(f"{test_name}: {status}")
        
        success_count = sum(1 for status in results.values() if "✅" in status)
        total_count = len(results)
        
        print(f"\n总计: {success_count}/{total_count} 个测试通过")
        
        if success_count == total_count:
            print("🎉 所有测试都通过了！")
        else:
            print("⚠️  部分测试失败，请检查配置和网络连接")

if __name__ == "__main__":
    tester = YesApiComprehensiveTest()
    tester.run_all_tests()

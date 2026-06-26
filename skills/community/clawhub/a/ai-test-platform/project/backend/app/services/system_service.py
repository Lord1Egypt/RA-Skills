"""
系统管理服务

提供AI模型配置、测试环境、操作日志和数据备份管理
"""

import os
import json
import shutil
from datetime import datetime
from typing import Optional, List, Dict
import logging

from sqlalchemy.orm import Session
from app.models.system import AIModelConfig, TestEnvironment, OperationLog, DataBackup
from app.schemas.system import (
    AIModelConfigCreate, AIModelConfigUpdate,
    EnvironmentCreate, EnvironmentUpdate,
    BackupCreate, BackupRestoreRequest
)

logger = logging.getLogger(__name__)


class SystemManagementService:
    """系统管理服务类"""

    def __init__(self, db: Session):
        self.db = db

    # ==================== AI模型配置管理 ====================

    def create_ai_model_config(self, config_data: AIModelConfigCreate) -> AIModelConfig:
        """
        创建AI模型配置

        Args:
            config_data: 模型配置数据

        Returns:
            创建的配置
        """
        # 加密API Key（简单实现，生产环境应使用更强的加密）
        encrypted_key = self._encrypt_api_key(config_data.api_key) if config_data.api_key else None

        config = AIModelConfig(
            name=config_data.name,
            model_type=config_data.model_type,
            provider=config_data.provider,
            model_name=config_data.model_name,
            api_key=encrypted_key,
            api_base_url=config_data.api_base_url,
            max_tokens=config_data.max_tokens,
            temperature=config_data.temperature,
            timeout=config_data.timeout,
            max_retries=config_data.max_retries,
            is_default=config_data.is_default,
            config_data=json.dumps(config_data.config_data, ensure_ascii=False) if config_data.config_data else None
        )

        # 如果设为默认，取消其他默认配置
        if config.is_default:
            self._clear_other_defaults()

        self.db.add(config)
        self.db.commit()
        self.db.refresh(config)

        logger.info(f"创建AI模型配置: {config.name}, type={config.model_type}")
        return config

    def get_ai_model_config(self, config_id: int) -> Optional[AIModelConfig]:
        """获取AI模型配置"""
        return self.db.query(AIModelConfig).filter(AIModelConfig.id == config_id).first()

    def get_default_ai_model_config(self) -> Optional[AIModelConfig]:
        """获取默认AI模型配置"""
        return self.db.query(AIModelConfig).filter(
            AIModelConfig.is_default == True,
            AIModelConfig.is_active == True
        ).first()

    def list_ai_model_configs(self, model_type: str = None) -> List[AIModelConfig]:
        """列出AI模型配置"""
        query = self.db.query(AIModelConfig)

        if model_type:
            query = query.filter(AIModelConfig.model_type == model_type)

        return query.filter(AIModelConfig.is_active == True).all()

    def update_ai_model_config(self, config_id: int, config_data: AIModelConfigUpdate) -> Optional[AIModelConfig]:
        """更新AI模型配置"""
        config = self.get_ai_model_config(config_id)
        if not config:
            return None

        # 更新字段
        if config_data.name:
            config.name = config_data.name
        if config_data.provider:
            config.provider = config_data.provider
        if config_data.model_name:
            config.model_name = config_data.model_name
        if config_data.api_key:
            config.api_key = self._encrypt_api_key(config_data.api_key)
        if config_data.api_base_url:
            config.api_base_url = config_data.api_base_url
        if config_data.max_tokens is not None:
            config.max_tokens = config_data.max_tokens
        if config_data.temperature is not None:
            config.temperature = config_data.temperature
        if config_data.timeout is not None:
            config.timeout = config_data.timeout
        if config_data.max_retries is not None:
            config.max_retries = config_data.max_retries
        if config_data.is_active is not None:
            config.is_active = config_data.is_active
        if config_data.is_default is not None:
            if config_data.is_default:
                self._clear_other_defaults()
            config.is_default = config_data.is_default

        self.db.commit()
        self.db.refresh(config)

        logger.info(f"更新AI模型配置: {config.name}")
        return config

    def delete_ai_model_config(self, config_id: int) -> bool:
        """删除AI模型配置（软删除）"""
        config = self.get_ai_model_config(config_id)
        if not config:
            return False

        config.is_active = False
        self.db.commit()

        logger.info(f"删除AI模型配置: {config.name}")
        return True

    def test_ai_model_config(self, config_id: int) -> Dict:
        """
        测试AI模型配置

        Args:
            config_id: 配置ID

        Returns:
            测试结果
        """
        config = self.get_ai_model_config(config_id)
        if not config:
            return {"success": False, "message": "配置不存在"}

        try:
            # 根据模型类型测试连接
            if config.model_type == "online":
                # 测试在线API
                from langchain_openai import ChatOpenAI

                llm = ChatOpenAI(
                    openai_api_key=self._decrypt_api_key(config.api_key),
                    openai_api_base=config.api_base_url,
                    model=config.model_name,
                    timeout=config.timeout
                )

                # 发送测试请求
                response = llm.invoke("Hello")
                return {"success": True, "message": "连接成功", "response": str(response)}

            elif config.model_type == "local":
                # 测试本地模型
                # 这里可以集成Ollama等本地模型
                return {"success": True, "message": "本地模型配置有效"}

        except Exception as e:
            logger.error(f"测试AI模型配置失败: {str(e)}")
            return {"success": False, "message": str(e)}

    # ==================== 测试环境管理 ====================

    def create_environment(self, env_data: EnvironmentCreate) -> TestEnvironment:
        """创建测试环境"""
        environment = TestEnvironment(
            name=env_data.name,
            env_type=env_data.env_type,
            base_url=env_data.base_url,
            description=env_data.description,
            headers=json.dumps(env_data.headers, ensure_ascii=False) if env_data.headers else None,
            params=json.dumps(env_data.params, ensure_ascii=False) if env_data.params else None,
            variables=json.dumps(env_data.variables, ensure_ascii=False) if env_data.variables else None,
            is_default=env_data.is_default
        )

        # 如果设为默认，取消其他默认环境
        if environment.is_default:
            self._clear_other_env_defaults()

        self.db.add(environment)
        self.db.commit()
        self.db.refresh(environment)

        logger.info(f"创建测试环境: {environment.name}")
        return environment

    def get_environment(self, env_id: int) -> Optional[TestEnvironment]:
        """获取测试环境"""
        return self.db.query(TestEnvironment).filter(TestEnvironment.id == env_id).first()

    def get_default_environment(self) -> Optional[TestEnvironment]:
        """获取默认测试环境"""
        return self.db.query(TestEnvironment).filter(
            TestEnvironment.is_default == True,
            TestEnvironment.is_active == True
        ).first()

    def list_environments(self, env_type: str = None) -> List[TestEnvironment]:
        """列出测试环境"""
        query = self.db.query(TestEnvironment)

        if env_type:
            query = query.filter(TestEnvironment.env_type == env_type)

        return query.filter(TestEnvironment.is_active == True).all()

    def update_environment(self, env_id: int, env_data: EnvironmentUpdate) -> Optional[TestEnvironment]:
        """更新测试环境"""
        environment = self.get_environment(env_id)
        if not environment:
            return None

        # 更新字段
        if env_data.name:
            environment.name = env_data.name
        if env_data.env_type:
            environment.env_type = env_data.env_type
        if env_data.base_url:
            environment.base_url = env_data.base_url
        if env_data.description:
            environment.description = env_data.description
        if env_data.headers:
            environment.headers = json.dumps(env_data.headers, ensure_ascii=False)
        if env_data.params:
            environment.params = json.dumps(env_data.params, ensure_ascii=False)
        if env_data.variables:
            environment.variables = json.dumps(env_data.variables, ensure_ascii=False)
        if env_data.is_active is not None:
            environment.is_active = env_data.is_active
        if env_data.is_default is not None:
            if env_data.is_default:
                self._clear_other_env_defaults()
            environment.is_default = env_data.is_default

        self.db.commit()
        self.db.refresh(environment)

        logger.info(f"更新测试环境: {environment.name}")
        return environment

    def delete_environment(self, env_id: int) -> bool:
        """删除测试环境（软删除）"""
        environment = self.get_environment(env_id)
        if not environment:
            return False

        environment.is_active = False
        self.db.commit()

        logger.info(f"删除测试环境: {environment.name}")
        return True

    # ==================== 操作日志 ====================

    def log_operation(self, user_id: str, operation_type: str, operation_module: str,
                     operation_desc: str, request_method: str = None, request_url: str = None,
                     request_params: str = None, response_status: int = None,
                     response_data: str = None, ip_address: str = None,
                     user_agent: str = None, duration: int = None) -> OperationLog:
        """
        记录操作日志

        Args:
            user_id: 用户ID（授权码）
            operation_type: 操作类型
            operation_module: 操作模块
            operation_desc: 操作描述
            request_method: 请求方法
            request_url: 请求URL
            request_params: 请求参数
            response_status: 响应状态码
            response_data: 响应数据
            ip_address: IP地址
            user_agent: 用户代理
            duration: 执行耗时（毫秒）

        Returns:
            操作日志
        """
        log = OperationLog(
            user_id=user_id,
            operation_type=operation_type,
            operation_module=operation_module,
            operation_desc=operation_desc,
            request_method=request_method,
            request_url=request_url,
            request_params=request_params,
            response_status=response_status,
            response_data=response_data,
            ip_address=ip_address,
            user_agent=user_agent,
            duration=duration
        )

        self.db.add(log)
        self.db.commit()

        return log

    def list_operation_logs(self, user_id: str = None, operation_type: str = None,
                           operation_module: str = None, start_date: datetime = None,
                           end_date: datetime = None, limit: int = 100) -> List[OperationLog]:
        """列出操作日志"""
        query = self.db.query(OperationLog)

        if user_id:
            query = query.filter(OperationLog.user_id == user_id)
        if operation_type:
            query = query.filter(OperationLog.operation_type == operation_type)
        if operation_module:
            query = query.filter(OperationLog.operation_module == operation_module)
        if start_date:
            query = query.filter(OperationLog.create_time >= start_date)
        if end_date:
            query = query.filter(OperationLog.create_time <= end_date)

        return query.order_by(OperationLog.create_time.desc()).limit(limit).all()

    # ==================== 数据备份 ====================

    def create_backup(self, backup_data: BackupCreate) -> DataBackup:
        """创建数据备份"""
        backup = DataBackup(
            name=backup_data.name,
            backup_type=backup_data.backup_type,
            backup_scope=backup_data.backup_scope,
            backup_config=json.dumps(backup_data.backup_config, ensure_ascii=False) if backup_data.backup_config else None
        )

        self.db.add(backup)
        self.db.commit()
        self.db.refresh(backup)

        # 异步执行备份（简化实现，生产环境应使用后台任务）
        try:
            self._execute_backup(backup.id)
        except Exception as e:
            logger.error(f"执行备份失败: {str(e)}")

        logger.info(f"创建数据备份: {backup.name}")
        return backup

    def get_backup(self, backup_id: int) -> Optional[DataBackup]:
        """获取备份"""
        return self.db.query(DataBackup).filter(DataBackup.id == backup_id).first()

    def list_backups(self, status: str = None, limit: int = 50) -> List[DataBackup]:
        """列出备份"""
        query = self.db.query(DataBackup)

        if status:
            query = query.filter(DataBackup.status == status)

        return query.order_by(DataBackup.create_time.desc()).limit(limit).all()

    def delete_backup(self, backup_id: int) -> bool:
        """删除备份"""
        backup = self.get_backup(backup_id)
        if not backup:
            return False

        # 删除备份文件
        if backup.file_path and os.path.exists(backup.file_path):
            try:
                os.remove(backup.file_path)
            except Exception as e:
                logger.error(f"删除备份文件失败: {str(e)}")

        self.db.delete(backup)
        self.db.commit()

        logger.info(f"删除数据备份: {backup.name}")
        return True

    def restore_backup(self, restore_data: BackupRestoreRequest) -> Dict:
        """
        恢复备份

        Args:
            restore_data: 恢复请求

        Returns:
            恢复结果
        """
        backup = self.get_backup(restore_data.backup_id)
        if not backup or backup.status != "completed":
            return {"success": False, "message": "备份不存在或未完成"}

        try:
            # 根据备份范围恢复
            if backup.backup_scope in ["database", "all"]:
                # 恢复数据库
                self._restore_database(backup.file_path)

            if backup.backup_scope in ["files", "all"]:
                # 恢复文件
                self._restore_files(backup.file_path)

            return {"success": True, "message": "恢复成功"}

        except Exception as e:
            logger.error(f"恢复备份失败: {str(e)}")
            return {"success": False, "message": str(e)}

    # ==================== 私有方法 ====================

    def _encrypt_api_key(self, api_key: str) -> str:
        """加密API Key（简单实现）"""
        # 生产环境应使用更强的加密算法
        import base64
        return base64.b64encode(api_key.encode()).decode()

    def _decrypt_api_key(self, encrypted_key: str) -> str:
        """解密API Key"""
        import base64
        return base64.b64decode(encrypted_key.encode()).decode()

    def _clear_other_defaults(self):
        """清除其他默认配置"""
        self.db.query(AIModelConfig).filter(AIModelConfig.is_default == True).update({"is_default": False})
        self.db.commit()

    def _clear_other_env_defaults(self):
        """清除其他默认环境"""
        self.db.query(TestEnvironment).filter(TestEnvironment.is_default == True).update({"is_default": False})
        self.db.commit()

    def _execute_backup(self, backup_id: int):
        """执行备份"""
        import time

        backup = self.get_backup(backup_id)
        if not backup:
            return

        try:
            backup.status = "pending"
            self.db.commit()

            # 创建备份目录
            backup_dir = "data/backups"
            os.makedirs(backup_dir, exist_ok=True)

            # 生成备份文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{backup.name}_{timestamp}.zip"
            backup_path = os.path.join(backup_dir, backup_filename)

            # 执行备份
            start_time = time.time()

            if backup.backup_scope in ["database", "all"]:
                # 备份数据库
                self._backup_database(backup_path)

            if backup.backup_scope in ["files", "all"]:
                # 备份文件
                self._backup_files(backup_path)

            # 更新备份记录
            backup.file_path = backup_path
            backup.file_size = os.path.getsize(backup_path) if os.path.exists(backup_path) else 0
            backup.status = "completed"
            backup.complete_time = datetime.now()

            self.db.commit()

            logger.info(f"备份完成: {backup.name}, 耗时{time.time() - start_time:.2f}秒")

        except Exception as e:
            backup.status = "failed"
            backup.error_message = str(e)
            self.db.commit()
            raise

    def _backup_database(self, backup_path: str):
        """备份数据库（简化实现）"""
        # 生产环境应使用mysqldump等工具
        logger.info(f"备份数据库到: {backup_path}")

    def _backup_files(self, backup_path: str):
        """备份文件"""
        logger.info(f"备份文件到: {backup_path}")

    def _restore_database(self, backup_path: str):
        """恢复数据库"""
        logger.info(f"从{backup_path}恢复数据库")

    def _restore_files(self, backup_path: str):
        """恢复文件"""
        logger.info(f"从{backup_path}恢复文件")

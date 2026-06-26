"""
备份恢复工具包 - 核心实现
Backup Recovery Toolkit - Core Implementation
"""

import os
import shutil
import hashlib
import json
import tarfile
import gzip
from datetime import datetime
from typing import Dict, List, Optional
import subprocess


class BackupResult:
    """备份结果类 | Backup result class"""
    
    def __init__(self):
        self.success = False
        self.files_backed_up = 0
        self.total_size = 0
        self.backup_path = ""
        self.timestamp = datetime.now().isoformat()
        self.errors = []
    
    def to_dict(self) -> Dict:
        """转换为字典 | Convert to dict"""
        return {
            'success': self.success,
            'files_backed_up': self.files_backed_up,
            'total_size': self.total_size,
            'backup_path': self.backup_path,
            'timestamp': self.timestamp,
            'errors': self.errors
        }


class FileBackup:
    """文件备份类 | File backup class"""
    
    def __init__(self, source: str, destination: str, compress: bool = True):
        """
        初始化文件备份器
        Initialize file backup
        
        Args:
            source: 源目录 | Source directory
            destination: 目标目录 | Destination directory
            compress: 是否压缩 | Whether to compress
        """
        self.source = os.path.abspath(source)
        self.destination = os.path.abspath(destination)
        self.compress = compress
        
        # 确保目标目录存在
        os.makedirs(self.destination, exist_ok=True)
    
    def run(self, name: Optional[str] = None) -> Dict:
        """
        执行备份
        Execute backup
        
        Args:
            name: 备份名称 | Backup name
            
        Returns:
            备份结果 | Backup result
        """
        result = BackupResult()
        
        try:
            # 生成备份名称
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = name or f"backup_{timestamp}"
            backup_path = os.path.join(self.destination, backup_name)
            
            if self.compress:
                backup_path += ".tar.gz"
                result = self._backup_compressed(backup_path)
            else:
                result = self._backup_uncompressed(backup_path)
            
            result.backup_path = backup_path
            result.success = True
            
        except Exception as e:
            result.errors.append(str(e))
        
        return result.to_dict()
    
    def _backup_compressed(self, backup_path: str) -> BackupResult:
        """压缩备份 | Compressed backup"""
        result = BackupResult()
        
        with tarfile.open(backup_path, "w:gz") as tar:
            for root, dirs, files in os.walk(self.source):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.source)
                    tar.add(file_path, arcname)
                    result.files_backed_up += 1
                    result.total_size += os.path.getsize(file_path)
        
        return result
    
    def _backup_uncompressed(self, backup_path: str) -> BackupResult:
        """非压缩备份 | Uncompressed backup"""
        result = BackupResult()
        os.makedirs(backup_path, exist_ok=True)
        
        for item in os.listdir(self.source):
            src = os.path.join(self.source, item)
            dst = os.path.join(backup_path, item)
            
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
                result.files_backed_up += 1
                result.total_size += os.path.getsize(src)
        
        return result


class IncrementalBackup(FileBackup):
    """增量备份类 | Incremental backup class"""
    
    def __init__(self, source: str, destination: str, reference_backup: Optional[str] = None):
        """
        初始化增量备份
        Initialize incremental backup
        
        Args:
            source: 源目录 | Source directory
            destination: 目标目录 | Destination directory
            reference_backup: 参考备份路径 | Reference backup path
        """
        super().__init__(source, destination)
        self.reference_backup = reference_backup
    
    def run(self, name: Optional[str] = None) -> Dict:
        """执行增量备份 | Execute incremental backup"""
        result = BackupResult()
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = (name or "incremental") + f"_{timestamp}"
            backup_path = os.path.join(self.destination, backup_name + ".tar.gz")
            
            # 获取已备份文件的哈希 | Get hashes of backed up files
            reference_hashes = self._get_reference_hashes()
            
            # 只备份变更的文件 | Only backup changed files
            with tarfile.open(backup_path, "w:gz") as tar:
                for root, dirs, files in os.walk(self.source):
                    for file in files:
                        file_path = os.path.join(root, file)
                        file_hash = self._get_file_hash(file_path)
                        
                        relative_path = os.path.relpath(file_path, self.source)
                        
                        # 如果文件是新的或已变更 | If file is new or changed
                        if relative_path not in reference_hashes or reference_hashes[relative_path] != file_hash:
                            tar.add(file_path, relative_path)
                            result.files_backed_up += 1
                            result.total_size += os.path.getsize(file_path)
            
            result.backup_path = backup_path
            result.success = True
            
        except Exception as e:
            result.errors.append(str(e))
        
        return result.to_dict()
    
    def _get_reference_hashes(self) -> Dict[str, str]:
        """获取参考备份中文件的哈希 | Get hashes from reference backup"""
        if not self.reference_backup or not os.path.exists(self.reference_backup):
            return {}
        
        hashes = {}
        try:
            with tarfile.open(self.reference_backup, "r:gz") as tar:
                for member in tar.getmembers():
                    if member.isfile():
                        f = tar.extractfile(member)
                        if f:
                            content = f.read()
                            hashes[member.name] = hashlib.md5(content).hexdigest()
        except Exception:
            pass
        
        return hashes
    
    @staticmethod
    def _get_file_hash(file_path: str) -> str:
        """计算文件MD5哈希 | Calculate file MD5 hash"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()


class DatabaseBackup:
    """数据库备份类 | Database backup class"""
    
    def __init__(self, db_type: str, host: str, user: str, password: str, 
                 database: str, port: Optional[int] = None):
        """
        初始化数据库备份
        Initialize database backup
        
        Args:
            db_type: 数据库类型 (mysql/postgresql/mongodb)
            host: 主机地址
            user: 用户名
            password: 密码
            database: 数据库名
            port: 端口 (可选)
        """
        self.db_type = db_type.lower()
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
    
    def run(self, destination: str) -> Dict:
        """
        执行数据库备份
        Execute database backup
        
        Args:
            destination: 备份文件保存路径
            
        Returns:
            备份结果
        """
        result = BackupResult()
        
        try:
            os.makedirs(os.path.dirname(destination) or '.', exist_ok=True)
            
            if self.db_type == 'mysql':
                result = self._backup_mysql(destination)
            elif self.db_type == 'postgresql':
                result = self._backup_postgresql(destination)
            elif self.db_type == 'mongodb':
                result = self._backup_mongodb(destination)
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")
            
            result.success = True
            
        except Exception as e:
            result.errors.append(str(e))
        
        return result.to_dict()
    
    def _backup_mysql(self, destination: str) -> BackupResult:
        """备份MySQL | Backup MySQL"""
        result = BackupResult()
        
        port = self.port or 3306
        cmd = [
            'mysqldump',
            '-h', self.host,
            '-P', str(port),
            '-u', self.user,
            f'-p{self.password}',
            self.database
        ]
        
        with open(destination, 'w') as f:
            subprocess.run(cmd, stdout=f, check=True)
        
        result.files_backed_up = 1
        result.total_size = os.path.getsize(destination)
        result.backup_path = destination
        
        return result
    
    def _backup_postgresql(self, destination: str) -> BackupResult:
        """备份PostgreSQL | Backup PostgreSQL"""
        result = BackupResult()
        
        port = self.port or 5432
        cmd = [
            'pg_dump',
            '-h', self.host,
            '-p', str(port),
            '-U', self.user,
            '-d', self.database,
            '-f', destination
        ]
        
        env = os.environ.copy()
        env['PGPASSWORD'] = self.password
        
        subprocess.run(cmd, env=env, check=True)
        
        result.files_backed_up = 1
        result.total_size = os.path.getsize(destination)
        result.backup_path = destination
        
        return result
    
    def _backup_mongodb(self, destination: str) -> BackupResult:
        """备份MongoDB | Backup MongoDB"""
        result = BackupResult()
        
        port = self.port or 27017
        cmd = [
            'mongodump',
            '--host', f'{self.host}:{port}',
            '--db', self.database,
            '-u', self.user,
            '-p', self.password,
            '--archive', destination,
            '--gzip'
        ]
        
        subprocess.run(cmd, check=True)
        
        result.files_backed_up = 1
        result.total_size = os.path.getsize(destination)
        result.backup_path = destination
        
        return result


class RestoreManager:
    """恢复管理类 | Restore manager class"""
    
    @staticmethod
    def restore_file_backup(backup_path: str, destination: str) -> Dict:
        """
        恢复文件备份
        Restore file backup
        
        Args:
            backup_path: 备份文件路径
            destination: 恢复目标路径
            
        Returns:
            恢复结果
        """
        result = {
            'success': False,
            'files_restored': 0,
            'errors': []
        }
        
        try:
            os.makedirs(destination, exist_ok=True)
            
            if backup_path.endswith('.tar.gz'):
                with tarfile.open(backup_path, "r:gz") as tar:
                    tar.extractall(destination)
                    result['files_restored'] = len(tar.getmembers())
            else:
                # 非压缩备份
                for item in os.listdir(backup_path):
                    src = os.path.join(backup_path, item)
                    dst = os.path.join(destination, item)
                    if os.path.isdir(src):
                        shutil.copytree(src, dst, dirs_exist_ok=True)
                    else:
                        shutil.copy2(src, dst)
                        result['files_restored'] += 1
            
            result['success'] = True
            
        except Exception as e:
            result['errors'].append(str(e))
        
        return result


if __name__ == '__main__':
    # 简单的命令行接口
    import argparse
    
    parser = argparse.ArgumentParser(description='Backup Recovery Toolkit')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # 备份命令
    backup_parser = subparsers.add_parser('backup', help='Full backup')
    backup_parser.add_argument('--source', required=True, help='Source directory')
    backup_parser.add_argument('--dest', required=True, help='Destination directory')
    backup_parser.add_argument('--name', help='Backup name')
    backup_parser.add_argument('--no-compress', action='store_true', help='Disable compression')
    
    # 增量备份命令
    incr_parser = subparsers.add_parser('incremental', help='Incremental backup')
    incr_parser.add_argument('--source', required=True, help='Source directory')
    incr_parser.add_argument('--dest', required=True, help='Destination directory')
    incr_parser.add_argument('--reference', help='Reference backup path')
    incr_parser.add_argument('--name', help='Backup name')
    
    # 恢复命令
    restore_parser = subparsers.add_parser('restore', help='Restore backup')
    restore_parser.add_argument('--backup', required=True, help='Backup file/directory')
    restore_parser.add_argument('--dest', required=True, help='Destination directory')
    
    args = parser.parse_args()
    
    if args.command == 'backup':
        backup = FileBackup(args.source, args.dest, not args.no_compress)
        result = backup.run(args.name)
        print(json.dumps(result, indent=2))
    
    elif args.command == 'incremental':
        backup = IncrementalBackup(args.source, args.dest, args.reference)
        result = backup.run(args.name)
        print(json.dumps(result, indent=2))
    
    elif args.command == 'restore':
        result = RestoreManager.restore_file_backup(args.backup, args.dest)
        print(json.dumps(result, indent=2))
    
    else:
        parser.print_help()

"""PipelineCheckpoint - 파이프라인 체크포인트 및 재개 기능

각 파이프라인 단계별 진행상태 저장, 실패 시 재개 지원
"""

import json
import logging
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any
from dataclasses import dataclass, field, asdict

logger = logging.getLogger('builder-agent.checkpoint')


@dataclass
class CheckpointState:
    """체크포인트 상태"""
    stage: str
    project_title: Optional[str] = None
    started_at: str = ""
    last_updated: str = ""
    retry_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    errors: list = field(default_factory=list)

    def __post_init__(self):
        if not self.started_at:
            self.started_at = datetime.now().isoformat()
        self.last_updated = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'CheckpointState':
        """딕셔너리에서 복원"""
        return cls(**data)


class PipelineCheckpoint:
    """파이프라인 체크포인트 관리자

    각 파이프라인 단계별 상태를 저장하고, 실패 시 마지막 체크포인트부터 재개
    """

    def __init__(self, checkpoint_dir: Path = None):
        """초기화

        Args:
            checkpoint_dir: 체크포인트 저장 경로 (기본: /tmp/builder-discovery/checkpoints)
        """
        if checkpoint_dir is None:
            checkpoint_dir = Path("/tmp/builder-discovery/checkpoints")

        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

        self._lock = threading.Lock()
        self._current_checkpoint: Optional[CheckpointState] = None

    def save_state(self, stage: str, state: Dict[str, Any]) -> bool:
        """현재 상태 저장

        Args:
            stage: 파이프라인 단계 (discovering, building, testing, etc.)
            state: 저장할 상태 정보

        Returns:
            성공 여부
        """
        try:
            with self._lock:
                # 현재 체크포인트 업데이트 또는 생성
                if self._current_checkpoint is None:
                    self._current_checkpoint = CheckpointState(stage=stage)

                # 상태 업데이트
                self._current_checkpoint.stage = stage
                self._current_checkpoint.last_updated = datetime.now().isoformat()
                self._current_checkpoint.metadata.update(state)

                # 파일로 저장
                checkpoint_path = self._get_checkpoint_path(stage)
                with open(checkpoint_path, 'w') as f:
                    json.dump(self._current_checkpoint.to_dict(), f, indent=2)

                logger.info("Checkpoint saved: %s at %s", stage, checkpoint_path)
                return True

        except Exception as e:
            logger.error("Failed to save checkpoint: %s", e)
            return False

    def load_last_checkpoint(self) -> Optional[CheckpointState]:
        """마지막 체크포인트 로드

        Returns:
            마지막 체크포인트 상태 또는 None
        """
        try:
            # 가장 최근 체크포인트 파일 찾기
            checkpoints = list(self.checkpoint_dir.glob("*.json"))
            if not checkpoints:
                return None

            # 수정 시간 기준 정렬
            latest = max(checkpoints, key=lambda p: p.stat().st_mtime)

            with open(latest, 'r') as f:
                data = json.load(f)

            checkpoint = CheckpointState.from_dict(data)
            self._current_checkpoint = checkpoint

            logger.info("Checkpoint loaded: %s from %s",
                       checkpoint.stage, latest)
            return checkpoint

        except Exception as e:
            logger.warning("Failed to load checkpoint: %s", e)
            return None

    def get_checkpoint(self, stage: str) -> Optional[CheckpointState]:
        """특정 스테이지의 체크포인트 로드

        Args:
            stage: 파이프라인 단계

        Returns:
            체크포인트 상태 또는 None
        """
        try:
            checkpoint_path = self._get_checkpoint_path(stage)
            if not checkpoint_path.exists():
                return None

            with open(checkpoint_path, 'r') as f:
                data = json.load(f)

            return CheckpointState.from_dict(data)

        except Exception as e:
            logger.warning("Failed to load checkpoint for %s: %s", stage, e)
            return None

    def increment_retry(self) -> int:
        """재시도 횟수 증가

        Returns:
            현재 재시도 횟수
        """
        if self._current_checkpoint:
            self._current_checkpoint.retry_count += 1
            self._current_checkpoint.last_updated = datetime.now().isoformat()

            # 저장
            stage = self._current_checkpoint.stage
            self.save_state(stage, self._current_checkpoint.metadata)

            return self._current_checkpoint.retry_count

        return 0

    def add_error(self, error: str):
        """에러 기록

        Args:
            error: 에러 메시지
        """
        if self._current_checkpoint:
            self._current_checkpoint.errors.append({
                'message': error,
                'timestamp': datetime.now().isoformat()
            })

            # 에러 추가 후 자동 저장
            if self._current_checkpoint.stage:
                self.save_state(self._current_checkpoint.stage, self._current_checkpoint.metadata)

    def clear_checkpoints(self, older_than_hours: int = 24):
        """오래된 체크포인트 정리

        Args:
            older_than_hours: 이 시간(시간)보다 오래된 체크포인트만 삭제
        """
        try:
            import time
            cutoff_time = time.time() - (older_than_hours * 3600)

            removed = 0
            for checkpoint_file in self.checkpoint_dir.glob("*.json"):
                if checkpoint_file.stat().st_mtime < cutoff_time:
                    checkpoint_file.unlink()
                    removed += 1

            logger.info("Cleared %d old checkpoints (older than %d hours)",
                       removed, older_than_hours)

        except Exception as e:
            logger.warning("Failed to clear checkpoints: %s", e)

    def _get_checkpoint_path(self, stage: str) -> Path:
        """체크포인트 파일 경로 생성"""
        # 프로젝트별로 분리하기 위해 project_title 사용
        project_title = self._current_checkpoint.project_title if self._current_checkpoint else "default"
        safe_title = (project_title or "default").replace(' ', '_').replace('/', '_')[:50]

        filename = f"{safe_title}_{stage}.json"
        return self.checkpoint_dir / filename

    def get_all_checkpoints(self) -> Dict[str, CheckpointState]:
        """모든 체크포인트 로드

        Returns:
            {stage: CheckpointState} 딕셔너리
        """
        checkpoints = {}

        try:
            for checkpoint_file in self.checkpoint_dir.glob("*.json"):
                try:
                    with open(checkpoint_file, 'r') as f:
                        data = json.load(f)

                    state = CheckpointState.from_dict(data)
                    # 파일명에서 stage 추출
                    stage = checkpoint_file.stem.split('_')[-1]
                    checkpoints[stage] = state

                except Exception as e:
                    logger.warning("Failed to load checkpoint %s: %s", checkpoint_file, e)

        except Exception as e:
            logger.warning("Failed to list checkpoints: %s", e)

        return checkpoints


class ProjectCheckpoint:
    """프로젝트별 체크포인트 관리

    여러 프로젝트를 병렬로 처리할 때 각 프로젝트의 상태를 독립적으로 관리
    """

    def __init__(self, project_title: str, checkpoint_dir: Path = None):
        """초기화

        Args:
            project_title: 프로젝트 제목
            checkpoint_dir: 체크포인트 저장 경로
        """
        self.project_title = project_title
        self.checkpoint = PipelineCheckpoint(checkpoint_dir)
        self.checkpoint._current_checkpoint = CheckpointState(
            stage="idle",
            project_title=project_title
        )

    def save_stage(self, stage: str, metadata: Dict[str, Any] = None) -> bool:
        """현재 스테이지 저장

        Args:
            stage: 파이프라인 단계
            metadata: 추가 메타데이터

        Returns:
            성공 여부
        """
        state = {
            'project_title': self.project_title,
            **(metadata or {})
        }
        return self.checkpoint.save_state(stage, state)

    def load_stage(self) -> Optional[CheckpointState]:
        """마지막 스테이지 로드

        Returns:
            체크포인트 상태 또는 None
        """
        return self.checkpoint.load_last_checkpoint()

    def can_resume(self) -> bool:
        """재개 가능한지 확인

        Returns:
            재개 가능 여부
        """
        last_checkpoint = self.checkpoint.load_last_checkpoint()
        if last_checkpoint and last_checkpoint.stage != "completed":
            return True
        return False

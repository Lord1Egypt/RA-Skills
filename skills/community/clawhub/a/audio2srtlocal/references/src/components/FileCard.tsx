import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  IconButton,
  LinearProgress,
  Tooltip,
  Box,
  Chip,
} from '@mui/material';
import CancelIcon from '@mui/icons-material/Cancel';
import RetryIcon from '@mui/icons-material/Replay';
import DeleteIcon from '@mui/icons-material/DeleteOutline';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import HourglassEmptyIcon from '@mui/icons-material/HourglassEmpty';
import LoadingIcon from '@mui/icons-material/Sync';
import TranscribeIcon from '@mui/icons-material/GraphicEq';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import BlockIcon from '@mui/icons-material/Block';
import { useQueueStore } from '../store/queueStore';
import {
  formatFileSize,
  formatDuration,
  getStatusColor,
  getStatusLabel,
  getLanguageLabel,
} from '../utils/helpers';
import type { TranscriptionTask } from '../types';

/** 任务卡片属性 */
interface TaskCardProps {
  task: TranscriptionTask;
}

/**
 * 转录任务卡片组件 — 展示任务信息和操作按钮。
 */
const TaskCard: React.FC<TaskCardProps> = ({ task }) => {
  const cancelTask = useQueueStore((s) => s.cancelTask);
  const retryTask = useQueueStore((s) => s.retryTask);
  const removeTask = useQueueStore((s) => s.removeTask);
  const selectTask = useQueueStore((s) => s.selectTask);
  const selectedTaskId = useQueueStore((s) => s.selectedTaskId);
  const isSelected = selectedTaskId === task.id;

  const statusColor = getStatusColor(task.status);
  const statusLabel = getStatusLabel(task.status);
  const isTranscribing = task.status === 'transcribing';

  /** 状态图标 */
  const StatusIcon: React.FC = () => {
    switch (task.status) {
      case 'queued':
        return <HourglassEmptyIcon sx={{ color: statusColor, fontSize: 20 }} />;
      case 'loading':
        return <LoadingIcon sx={{ color: statusColor, fontSize: 20, animation: 'spin 1s linear infinite' }} />;
      case 'transcribing':
        return <TranscribeIcon sx={{ color: statusColor, fontSize: 20, animation: 'pulse-glow 1.5s ease-in-out infinite' }} />;
      case 'completed':
        return <CheckCircleIcon sx={{ color: statusColor, fontSize: 20 }} />;
      case 'failed':
        return <ErrorIcon sx={{ color: statusColor, fontSize: 20 }} />;
      case 'cancelled':
        return <BlockIcon sx={{ color: statusColor, fontSize: 20 }} />;
      default:
        return null;
    }
  };

  return (
    <Card
      className="animate-slide-up"
      onClick={() => {
        if (task.status === 'completed' || task.status === 'transcribing') {
          selectTask(isSelected ? null : task.id);
        }
      }}
      sx={{
        mb: 1.5,
        borderRadius: 2,
        overflow: 'visible',
        position: 'relative',
        cursor: task.status === 'completed' || task.status === 'transcribing' ? 'pointer' : 'default',
        outline: isSelected ? '2px solid #7C4DFF' : 'none',
        outlineOffset: -1,
        bgcolor: isSelected ? 'rgba(124, 77, 255, 0.06)' : undefined,
        '&:hover': (task.status === 'completed' || task.status === 'transcribing')
          ? { bgcolor: isSelected ? 'rgba(124, 77, 255, 0.08)' : 'rgba(42, 47, 74, 0.3)' }
          : undefined,
      }}
    >
      {/* 顶部状态色条 */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: 3,
          bgcolor: statusColor,
          borderRadius: '12px 12px 0 0',
          opacity: isTranscribing ? 1 : 0.6,
          ...(isTranscribing && {
            animation: 'pulse-bar 1.5s ease-in-out infinite',
          }),
        }}
      />

      <CardContent sx={{ py: 2, px: 2.5, '&:last-child': { pb: 2 } }}>
        {/* 文件信息行 */}
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1 min-w-0">
            <Typography
              variant="body1"
              sx={{
                fontWeight: 600,
                color: '#E8EAF0',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap',
              }}
            >
              {task.fileName}
            </Typography>

            {/* 元信息标签 */}
            <div className="flex items-center gap-2 mt-1 flex-wrap">
              <Typography variant="caption" sx={{ color: '#5A6180' }}>
                {formatFileSize(task.fileSize)}
              </Typography>
              <Typography variant="caption" sx={{ color: '#3D4266' }}>
                ·
              </Typography>
              <Typography variant="caption" sx={{ color: '#5A6180' }}>
                {formatDuration(task.duration ?? 0)}
              </Typography>
              <Chip
                label={getLanguageLabel(task.language)}
                size="small"
                sx={{
                  height: 20,
                  fontSize: '0.65rem',
                  bgcolor: 'rgba(124, 77, 255, 0.15)',
                  color: '#B388FF',
                  fontWeight: 600,
                }}
              />
              <Chip
                label={task.model}
                size="small"
                sx={{
                  height: 20,
                  fontSize: '0.6rem',
                  bgcolor: 'rgba(33, 150, 243, 0.12)',
                  color: '#64B5F6',
                  fontWeight: 500,
                }}
              />
            </div>
          </div>

          {/* 状态标签 */}
          <div className="flex items-center gap-1.5 shrink-0">
            <StatusIcon />
            <Typography
              variant="caption"
              sx={{
                color: statusColor,
                fontWeight: 700,
                fontSize: '0.75rem',
                letterSpacing: '0.02em',
              }}
            >
              {statusLabel}
            </Typography>
          </div>
        </div>

        {/* Chunk 进度条区域 */}
        {(task.status === 'loading' ||
          task.status === 'transcribing' ||
          task.progress > 0) && (
          <div className="mt-2">
            <div className="flex items-center justify-between mb-1">
              <Typography variant="caption" sx={{ color: '#77809A' }}>
                {task.status === 'loading'
                  ? '转录中...'
                  : task.skippedChunks > 0
                    ? `第 ${task.currentChunk}/${task.totalChunks} 段（跳过 ${task.skippedChunks} 段）`
                    : `第 ${task.currentChunk}/${task.totalChunks} 段`}
              </Typography>
              <Typography
                variant="caption"
                sx={{ color: statusColor, fontWeight: 700, minWidth: 36, textAlign: 'right' }}
              >
                {task.progress}%
              </Typography>
            </div>
            <LinearProgress
              variant="determinate"
              value={task.progress}
              sx={{
                height: 6,
                borderRadius: 3,
                bgcolor: 'rgba(90, 97, 128, 0.3)',
                '& .MuiLinearProgress-bar': {
                  borderRadius: 3,
                  background:
                    task.status === 'loading'
                      ? 'linear-gradient(90deg, #2196F3, #64B5F6)'
                      : task.status === 'transcribing'
                        ? 'linear-gradient(90deg, #FF9800, #FFB74D)'
                        : `linear-gradient(90deg, ${statusColor}, ${statusColor}CC)`,
                  transition: 'width 0.3s ease',
                },
              }}
            />
          </div>
        )}

        {/* 错误信息 */}
        {task.status === 'failed' && task.error && (
          <Typography variant="caption" sx={{ color: '#F44336', mt: 1, display: 'block' }}>
            {task.error}
          </Typography>
        )}

        {/* 输出 SRT 路径 */}
        {task.status === 'completed' && task.outputSrtPath && (
          <div className="mt-1">
            <Typography
              variant="caption"
              sx={{ color: '#4CAF50', opacity: 0.8 }}
            >
              输出：{task.outputSrtPath}
            </Typography>
            {task.skippedChunks > 0 && (
              <Typography
                variant="caption"
                sx={{ color: '#FF9800', ml: 1.5 }}
              >
                ⚠️ 跳过 {task.skippedChunks} 段（推理异常）
              </Typography>
            )}
          </div>
        )}

        {/* 操作按钮 */}
        <div className="flex items-center gap-0.5 mt-2 -mr-1">
          {(task.status === 'queued' ||
            task.status === 'loading' ||
            task.status === 'transcribing') && (
            <Tooltip title="取消">
              <IconButton
                size="small"
                onClick={() => cancelTask(task.id)}
                sx={{ color: '#F44336' }}
              >
                <CancelIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          )}

          {task.status === 'failed' && (
            <Tooltip title="重试">
              <IconButton
                size="small"
                onClick={() => retryTask(task.id)}
                sx={{ color: '#7C4DFF' }}
              >
                <RetryIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          )}

          {(task.status === 'completed' ||
            task.status === 'failed' ||
            task.status === 'cancelled') && (
            <Tooltip title="删除">
              <IconButton
                size="small"
                onClick={() => removeTask(task.id)}
                sx={{ color: '#5A6180' }}
              >
                <DeleteIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          )}

          {task.status === 'completed' && task.outputSrtPath && (
            <Tooltip title="打开 SRT 文件">
              <IconButton
                size="small"
                sx={{ color: '#4CAF50' }}
              >
                <OpenInNewIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          )}
        </div>
      </CardContent>

      {/* 动画样式 */}
      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        @keyframes pulse-glow {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.6; transform: scale(1.15); }
        }
        @keyframes pulse-bar {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
      `}</style>
    </Card>
  );
};

export default TaskCard as React.FC<TaskCardProps>;

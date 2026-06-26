import React, { useState } from 'react';
import {
  Box,
  Typography,
  Chip,
  Button,
} from '@mui/material';
import FilterListIcon from '@mui/icons-material/FilterList';
import DeleteSweepIcon from '@mui/icons-material/DeleteSweep';
import TaskCard from './FileCard';
import { useQueueStore } from '../store/queueStore';
import type { TranscriptionTask, FilterTab } from '../types';

/** 筛选标签配置 */
const FILTER_TABS: { key: FilterTab; label: string }[] = [
  { key: 'all', label: '全部' },
  { key: 'transcribing', label: '转录中' },
  { key: 'completed', label: '已完成' },
  { key: 'failed', label: '失败' },
];

/** 文件列表属性 */
interface FileListProps {
  tasks: TranscriptionTask[];
}

/**
 * 文件列表组件 — 带筛选标签和清空操作。
 */
const FileList: React.FC<FileListProps> = ({ tasks }) => {
  const [activeFilter, setActiveFilter] = useState<FilterTab>('all');
  const clearCompleted = useQueueStore((s) => s.clearCompleted);
  const getFilteredTasks = useQueueStore((s) => s.getFilteredTasks);

  const filteredTasks = getFilteredTasks(activeFilter);

  const completedOrCancelledCount = tasks.filter(
    (t) => t.status === 'completed' || t.status === 'cancelled',
  ).length;

  return (
    <Box>
      {/* 筛选栏 */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-1.5">
          <FilterListIcon sx={{ fontSize: 18, color: '#5A6180', mr: 0.5 }} />
          {FILTER_TABS.map((tab) => (
            <Chip
              key={tab.key}
              label={tab.label}
              size="small"
              onClick={() => setActiveFilter(tab.key)}
              sx={{
                height: 28,
                fontSize: '0.75rem',
                fontWeight: 600,
                cursor: 'pointer',
                bgcolor:
                  activeFilter === tab.key
                    ? 'rgba(124, 77, 255, 0.2)'
                    : 'rgba(42, 47, 74, 0.6)',
                color: activeFilter === tab.key ? '#B388FF' : '#9EA3B8',
                border:
                  activeFilter === tab.key
                    ? '1px solid rgba(124, 77, 255, 0.4)'
                    : '1px solid transparent',
                '&:hover': {
                  bgcolor: 'rgba(124, 77, 255, 0.15)',
                  color: '#B388FF',
                },
              }}
            />
          ))}
        </div>

        {completedOrCancelledCount > 0 && (
          <Button
            size="small"
            startIcon={<DeleteSweepIcon />}
            onClick={clearCompleted}
            sx={{
              color: '#5A6180',
              fontSize: '0.75rem',
              '&:hover': { color: '#F44336' },
            }}
          >
            清空已完成
          </Button>
        )}
      </div>

      {/* 任务列表 */}
      {filteredTasks.length === 0 ? (
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            py: 8,
            color: '#5A6180',
          }}
        >
          <Typography variant="body1" sx={{ opacity: 0.6 }}>
            {activeFilter === 'all'
              ? '拖拽音频文件到上方区域开始转录'
              : '暂无匹配的任务'}
          </Typography>
        </Box>
      ) : (
        filteredTasks.map((task) => <TaskCard key={task.id} task={task} />)
      )}
    </Box>
  );
};

export default FileList;

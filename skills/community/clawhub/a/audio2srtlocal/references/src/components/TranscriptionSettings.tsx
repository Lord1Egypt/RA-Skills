import React, { useState, useRef, useCallback } from 'react';
import {
  Box,
  Typography,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Slider,
  Collapse,
  IconButton,
  Tooltip,
  Divider,
  Chip,
} from '@mui/material';
import SettingsIcon from '@mui/icons-material/Tune';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import FolderOpenIcon from '@mui/icons-material/FolderOpen';
import CloudDoneIcon from '@mui/icons-material/CloudDone';
import CloudOffIcon from '@mui/icons-material/CloudOff';
import { useQueueStore } from '../store/queueStore';
import { LANGUAGES } from '../utils/helpers';
import type { AppSettings } from '../types';

/**
 * 转录参数设置面板 — 可折叠，包含语言、模型、分段等设置。
 */
const TranscriptionSettings: React.FC = () => {
  const [expanded, setExpanded] = useState(true);
  const settings = useQueueStore((s) => s.settings);
  const updateSettings = useQueueStore((s) => s.updateSettings);
  const backendConnected = useQueueStore((s) => s.backendConnected);
  const checkBackend = useQueueStore((s) => s.checkBackend);
  const defaultWhisperModelName = useQueueStore((s) => s.defaultWhisperModelName);
  const defaultTranslateModelName = useQueueStore((s) => s.defaultTranslateModelName);

  /** 隐藏的目录选择 input（输出目录） */
  const outputDirInputRef = useRef<HTMLInputElement>(null);
  /** 隐藏的目录选择 input（Whisper 模型路径） */
  const modelDirInputRef = useRef<HTMLInputElement>(null);
  /** 隐藏的目录选择 input（翻译模型路径） */
  const translateModelDirInputRef = useRef<HTMLInputElement>(null);

  const handleChange = (field: keyof AppSettings, value: string | number) => {
    updateSettings({ [field]: value } as Partial<AppSettings>);
  };

  /** 处理输出目录选择 */
  const handleOutputDirPick = useCallback(async () => {
    if ('showDirectoryPicker' in window) {
      try {
        const dirHandle = await (window as any).showDirectoryPicker({ mode: 'read' });
        if (dirHandle) {
          const currentDir = settings.outputDir;
          const homePrefix = currentDir.startsWith('~/') ? '~/' : '';
          const newPath = homePrefix ? `~/${dirHandle.name}` : dirHandle.name;
          updateSettings({ outputDir: newPath });
          return;
        }
      } catch (e: any) {
        if (e?.name === 'AbortError') return;
      }
    }
    outputDirInputRef.current?.click();
  }, [settings.outputDir, updateSettings]);

  const handleOutputDirInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const files = e.target.files;
      if (files && files.length > 0) {
        const relPath = files[0].webkitRelativePath;
        const dirName = relPath.split('/')[0];
        const currentDir = settings.outputDir;
        const homePrefix = currentDir.startsWith('~/') ? '~/' : '';
        updateSettings({ outputDir: homePrefix ? `~/${dirName}` : dirName });
      }
      e.target.value = '';
    },
    [settings.outputDir, updateSettings],
  );

  const handleModelDirPick = useCallback(async () => {
    if ('showDirectoryPicker' in window) {
      try {
        const dirHandle = await (window as any).showDirectoryPicker({ mode: 'read' });
        if (dirHandle) {
          updateSettings({ modelPath: dirHandle.name });
          return;
        }
      } catch (e: any) {
        if (e?.name === 'AbortError') return;
      }
    }
    modelDirInputRef.current?.click();
  }, [updateSettings]);

  const handleModelDirInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const files = e.target.files;
      if (files && files.length > 0) {
        const relPath = files[0].webkitRelativePath;
        const dirName = relPath.split('/')[0];
        updateSettings({ modelPath: dirName });
      }
      e.target.value = '';
    },
    [updateSettings],
  );

  /** 翻译模型目录选择 */
  const handleTranslateModelDirPick = useCallback(async () => {
    if ('showDirectoryPicker' in window) {
      try {
        const dirHandle = await (window as any).showDirectoryPicker({ mode: 'read' });
        if (dirHandle) {
          updateSettings({ translateModel: dirHandle.name });
          return;
        }
      } catch (e: any) {
        if (e?.name === 'AbortError') return;
      }
    }
    translateModelDirInputRef.current?.click();
  }, [updateSettings]);

  const handleTranslateModelDirInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const files = e.target.files;
      if (files && files.length > 0) {
        const relPath = files[0].webkitRelativePath;
        const dirName = relPath.split('/')[0];
        updateSettings({ translateModel: dirName });
      }
      e.target.value = '';
    },
    [updateSettings],
  );

  return (
    <Box
      sx={{
        bgcolor: 'rgba(30, 34, 54, 0.6)',
        borderRadius: 2,
        border: '1px solid rgba(124, 77, 255, 0.1)',
        overflow: 'hidden',
      }}
    >
      {/* 折叠头部 */}
      <div
        className="flex items-center justify-between px-3 py-2 cursor-pointer"
        onClick={() => setExpanded(!expanded)}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') setExpanded(!expanded);
        }}
      >
        <div className="flex items-center gap-2">
          <SettingsIcon sx={{ fontSize: 20, color: '#7C4DFF' }} />
          <Typography variant="body2" sx={{ color: '#B388FF', fontWeight: 600 }}>
            转录参数设置
          </Typography>
        </div>
        <div className="flex items-center gap-2">
          {/* 后端连接状态 */}
          <Chip
            icon={backendConnected ? <CloudDoneIcon /> : <CloudOffIcon />}
            label={backendConnected ? '已连接' : '未连接'}
            size="small"
            onClick={(e) => {
              e.stopPropagation();
              checkBackend();
            }}
            sx={{
              height: 22,
              fontSize: '0.7rem',
              bgcolor: backendConnected ? 'rgba(76,175,80,0.15)' : 'rgba(244,67,54,0.15)',
              color: backendConnected ? '#4CAF50' : '#F44336',
              border: `1px solid ${backendConnected ? 'rgba(76,175,80,0.3)' : 'rgba(244,67,54,0.3)'}`,
              '& .MuiChip-icon': { color: backendConnected ? '#4CAF50' : '#F44336', fontSize: 14 },
            }}
          />
          <IconButton size="small" sx={{ color: '#5A6180' }}>
            {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
          </IconButton>
        </div>
      </div>

      {/* 折叠内容 */}
      <Collapse in={expanded}>
        <Divider sx={{ borderColor: 'rgba(124, 77, 255, 0.1)' }} />
        <Box sx={{ p: 2.5, display: 'flex', flexDirection: 'column', gap: 2.5 }}>
          {/* 后端 API 地址 */}
          <TextField
            size="small"
            label="后端 API 地址"
            value={settings.apiBaseUrl}
            onChange={(e) => handleChange('apiBaseUrl', e.target.value)}
            sx={{
              '& .MuiOutlinedInput-root': {
                color: '#E8EAF0',
                bgcolor: 'rgba(42, 47, 74, 0.6)',
                borderRadius: 1.5,
                fontSize: '0.85rem',
                '& fieldset': { borderColor: 'rgba(124, 77, 255, 0.2)' },
                '&:hover fieldset': { borderColor: 'rgba(124, 77, 255, 0.4)' },
                '&.Mui-focused fieldset': { borderColor: '#7C4DFF' },
              },
              '& .MuiInputLabel-root': {
                color: '#9EA3B8',
                '&.Mui-focused': { color: '#7C4DFF' },
              },
            }}
          />

          {/* 第一行：语言 + 模型路径 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {/* 语言选择 */}
            <FormControl size="small" fullWidth>
              <InputLabel sx={{ color: '#9EA3B8' }}>默认语言</InputLabel>
              <Select
                value={settings.defaultLanguage}
                label="默认语言"
                onChange={(e) => handleChange('defaultLanguage', e.target.value)}
                sx={{
                  color: '#E8EAF0',
                  bgcolor: 'rgba(42, 47, 74, 0.6)',
                  borderRadius: 1.5,
                  '& .MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(124, 77, 255, 0.2)' },
                  '&:hover .MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(124, 77, 255, 0.4)' },
                  '&.Mui-focused .MuiOutlinedInput-notchedOutline': { borderColor: '#7C4DFF' },
                  '& .MuiSelect-icon': { color: '#9EA3B8' },
                }}
              >
                {LANGUAGES.map((lang) => (
                  <MenuItem key={lang.code} value={lang.code}>
                    <span className="flex items-center gap-2">
                      <span className="font-semibold">{lang.label}</span>
                      {lang.code !== 'auto' && (
                        <span className="text-gray-400 text-xs">({lang.code})</span>
                      )}
                    </span>
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            {/* 模型路径 */}
            <TextField
              size="small"
              label="Whisper 模型路径"
              placeholder={defaultWhisperModelName ? `默认: ${defaultWhisperModelName}` : '留空使用服务器默认'}
              value={settings.modelPath}
              onChange={(e) => handleChange('modelPath', e.target.value)}
              InputProps={{
                endAdornment: (
                  <Tooltip title="浏览模型目录">
                    <IconButton size="small" sx={{ color: '#7C4DFF' }} onClick={handleModelDirPick}>
                      <FolderOpenIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                ),
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  color: '#E8EAF0',
                  bgcolor: 'rgba(42, 47, 74, 0.6)',
                  borderRadius: 1.5,
                  '& fieldset': { borderColor: 'rgba(124, 77, 255, 0.2)' },
                  '&:hover fieldset': { borderColor: 'rgba(124, 77, 255, 0.4)' },
                  '&.Mui-focused fieldset': { borderColor: '#7C4DFF' },
                },
                '& .MuiInputLabel-root': {
                  color: '#9EA3B8',
                  '&.Mui-focused': { color: '#7C4DFF' },
                },
              }}
            />
          </div>

          {/* 第二行：Chunk 秒数 + 重叠秒数 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <Box>
              <div className="flex items-center justify-between mb-1">
                <Typography variant="caption" sx={{ color: '#9EA3B8' }}>分段秒数</Typography>
                <TextField
                  size="small"
                  type="number"
                  value={settings.defaultChunkSec}
                  onChange={(e) => {
                    const val = parseInt(e.target.value, 10);
                    if (!isNaN(val) && val >= 60 && val <= 1800) handleChange('defaultChunkSec', val);
                  }}
                  inputProps={{ min: 60, max: 1800, step: 30, style: { textAlign: 'center', padding: '2px 6px' } }}
                  sx={{
                    width: 80,
                    '& .MuiOutlinedInput-root': {
                      color: '#E8EAF0', bgcolor: 'rgba(42, 47, 74, 0.6)', fontSize: '0.8rem',
                      '& fieldset': { borderColor: 'rgba(124, 77, 255, 0.2)' },
                    },
                  }}
                />
              </div>
              <Slider
                value={settings.defaultChunkSec}
                onChange={(_, val) => handleChange('defaultChunkSec', val as number)}
                min={60} max={1800} step={30}
                valueLabelDisplay="auto" valueLabelFormat={(v) => `${v}s`}
                sx={{
                  color: '#7C4DFF',
                  '& .MuiSlider-thumb': { '&:hover': { boxShadow: '0 0 0 8px rgba(124, 77, 255, 0.16)' } },
                  '& .MuiSlider-valueLabel': { bgcolor: '#7C4DFF' },
                }}
              />
              <div className="flex justify-between">
                <Typography variant="caption" sx={{ color: '#5A6180' }}>60s</Typography>
                <Typography variant="caption" sx={{ color: '#5A6180' }}>1800s</Typography>
              </div>
            </Box>

            <Box>
              <div className="flex items-center justify-between mb-1">
                <Typography variant="caption" sx={{ color: '#9EA3B8' }}>重叠秒数</Typography>
                <TextField
                  size="small"
                  type="number"
                  value={settings.defaultOverlapSec}
                  onChange={(e) => {
                    const val = parseInt(e.target.value, 10);
                    if (!isNaN(val) && val >= 0 && val <= 120) handleChange('defaultOverlapSec', val);
                  }}
                  inputProps={{ min: 0, max: 120, step: 5, style: { textAlign: 'center', padding: '2px 6px' } }}
                  sx={{
                    width: 80,
                    '& .MuiOutlinedInput-root': {
                      color: '#E8EAF0', bgcolor: 'rgba(42, 47, 74, 0.6)', fontSize: '0.8rem',
                      '& fieldset': { borderColor: 'rgba(124, 77, 255, 0.2)' },
                    },
                  }}
                />
              </div>
              <Slider
                value={settings.defaultOverlapSec}
                onChange={(_, val) => handleChange('defaultOverlapSec', val as number)}
                min={0} max={120} step={5}
                valueLabelDisplay="auto" valueLabelFormat={(v) => `${v}s`}
                sx={{
                  color: '#FF9800',
                  '& .MuiSlider-thumb': { '&:hover': { boxShadow: '0 0 0 8px rgba(255, 152, 0, 0.16)' } },
                  '& .MuiSlider-valueLabel': { bgcolor: '#FF9800' },
                }}
              />
              <div className="flex justify-between">
                <Typography variant="caption" sx={{ color: '#5A6180' }}>0s</Typography>
                <Typography variant="caption" sx={{ color: '#5A6180' }}>120s</Typography>
              </div>
            </Box>
          </div>

          {/* 第三行：输出目录 + 翻译模型 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <TextField
              size="small"
              label="输出目录"
              value={settings.outputDir}
              onChange={(e) => handleChange('outputDir', e.target.value)}
              InputProps={{
                endAdornment: (
                  <Tooltip title="选择输出目录">
                    <IconButton size="small" sx={{ color: '#7C4DFF' }} onClick={handleOutputDirPick}>
                      <FolderOpenIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                ),
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  color: '#E8EAF0', bgcolor: 'rgba(42, 47, 74, 0.6)', borderRadius: 1.5,
                  '& fieldset': { borderColor: 'rgba(124, 77, 255, 0.2)' },
                  '&:hover fieldset': { borderColor: 'rgba(124, 77, 255, 0.4)' },
                  '&.Mui-focused fieldset': { borderColor: '#7C4DFF' },
                },
                '& .MuiInputLabel-root': { color: '#9EA3B8', '&.Mui-focused': { color: '#7C4DFF' } },
              }}
            />

            <TextField
              size="small"
              label="翻译模型"
              placeholder={defaultTranslateModelName ? `默认: ${defaultTranslateModelName}` : '留空使用服务器默认'}
              value={settings.translateModel}
              onChange={(e) => handleChange('translateModel', e.target.value)}
              InputProps={{
                endAdornment: (
                  <Tooltip title="浏览翻译模型目录">
                    <IconButton size="small" sx={{ color: '#7C4DFF' }} onClick={handleTranslateModelDirPick}>
                      <FolderOpenIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                ),
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  color: '#E8EAF0', bgcolor: 'rgba(42, 47, 74, 0.6)', borderRadius: 1.5,
                  '& fieldset': { borderColor: 'rgba(124, 77, 255, 0.2)' },
                  '&:hover fieldset': { borderColor: 'rgba(124, 77, 255, 0.4)' },
                  '&.Mui-focused fieldset': { borderColor: '#7C4DFF' },
                },
                '& .MuiInputLabel-root': { color: '#9EA3B8', '&.Mui-focused': { color: '#7C4DFF' } },
              }}
            />
          </div>
        </Box>
      </Collapse>

      {/* 隐藏的目录选择 input（回退） */}
      <input ref={outputDirInputRef} type="file" style={{ display: 'none' }} {...{ webkitdirectory: '', directory: '' }} onChange={handleOutputDirInputChange} />
      <input ref={modelDirInputRef} type="file" style={{ display: 'none' }} {...{ webkitdirectory: '', directory: '' }} onChange={handleModelDirInputChange} />
      <input ref={translateModelDirInputRef} type="file" style={{ display: 'none' }} {...{ webkitdirectory: '', directory: '' }} onChange={handleTranslateModelDirInputChange} />
    </Box>
  );
};

export default TranscriptionSettings;

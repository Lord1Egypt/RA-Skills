import React from 'react';
import { CssBaseline, ThemeProvider, createTheme, Box, Container } from '@mui/material';
import Header from './components/Header';
import TranscriptionSettings from './components/TranscriptionSettings';
import DropZone from './components/DropZone';
import FileList from './components/FileList';
import StatsBar from './components/StatsBar';
import ResultPanel from './components/ResultPanel';
import SrtTranslatePage from './components/SrtTranslatePage';
import { useQueueStore } from './store/queueStore';

/** MUI 深色主题配置 — 蓝紫主色调 */
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#7C4DFF' },
    secondary: { main: '#B388FF' },
    success: { main: '#4CAF50' },
    warning: { main: '#FF9800' },
    error: { main: '#F44336' },
    background: {
      default: '#0D0F1A',
      paper: '#1E2236',
    },
    text: {
      primary: '#E8EAF0',
      secondary: '#9EA3B8',
    },
  },
  typography: {
    fontFamily:
      "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
        },
      },
    },
  },
});

/**
 * 应用主组件 — MLX Whisper 转录队列管理工具。
 * 支持两个页面：转录队列 / SRT 翻译。
 */
const App: React.FC = () => {
  const currentPage = useQueueStore((s) => s.currentPage);
  const tasks = useQueueStore((s) => s.tasks);
  const selectedTaskId = useQueueStore((s) => s.selectedTaskId);
  const showResultPanel = selectedTaskId !== null;

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column', bgcolor: 'background.default' }}>
        <Header />

        {currentPage === 'transcribe' ? (
          /* ── 转录队列页面 ───────────────────────── */
          <Box sx={{ flex: 1, overflowY: 'auto' }}>
          <Container
            maxWidth={false}
            sx={{
              py: 3,
              px: { xs: 2, md: 3 },
              maxWidth: showResultPanel ? '100%' : 'lg',
              mx: showResultPanel ? 0 : 'auto',
            }}
          >
            <div className={showResultPanel ? 'grid grid-cols-1 lg:grid-cols-2 gap-4' : ''}>
              {/* 左侧：队列管理区 */}
              <div>
                {/* 转录参数设置（折叠区） */}
                <div className="mb-4">
                  <TranscriptionSettings />
                </div>

                {/* 拖拽上传区 */}
                <div className="mb-4">
                  <DropZone />
                </div>

                {/* 统计面板 */}
                <StatsBar />

                {/* 任务列表（含筛选） */}
                <div className="mt-4">
                  <FileList tasks={tasks} />
                </div>
              </div>

              {/* 右侧：转录结果面板 */}
              {showResultPanel && (
                <Box
                  sx={{
                    position: 'sticky',
                    top: 0,
                    height: 'calc(100vh - 80px)',
                    minHeight: 400,
                  }}
                >
                  <ResultPanel />
                </Box>
              )}
            </div>
          </Container>
          </Box>
        ) : (
          /* ── SRT 翻译页面 ───────────────────────── */
          <Box sx={{ flex: 1, overflow: 'hidden' }}>
            <SrtTranslatePage />
          </Box>
        )}
      </Box>
    </ThemeProvider>
  );
};

export default App;

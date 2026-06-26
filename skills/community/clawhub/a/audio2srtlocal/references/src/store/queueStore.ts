import { create } from 'zustand';
import type {
  TranscriptionTask,
  TaskStatus,
  AppSettings,
  QueueStats,
  PageName,
} from '../types';
import {
  generateId,
  getShortModelName,
  apiStartTranscription,
  apiGetTaskStatus,
  apiCancelTask,
  apiUploadFile,
  apiTranslate,
  parseSrt,
  exportSegmentsToSrt,
  downloadSrt,
  formatSrtTime,
} from '../utils/helpers';

/**
 * 轮询定时器映射。
 * key: 任务 ID, value: intervalId
 */
const pollingTimers = new Map<string, ReturnType<typeof setInterval>>();

/** 轮询间隔（毫秒） */
const POLL_INTERVAL = 1500;

/** SRT 翻译的 AbortController，用于停止翻译 */
let srtAbortController: AbortController | null = null;

/**
 * 队列状态管理 Store
 */
interface QueueStore {
  /** 当前页面 */
  currentPage: PageName;

  /** 任务列表 */
  tasks: TranscriptionTask[];

  /** 全局设置 */
  settings: AppSettings;

  /** 当前选中的任务 ID（右侧面板显示） */
  selectedTaskId: string | null;

  /** 后端连接状态 */
  backendConnected: boolean;

  /** 后端默认模型名称（从 health 接口获取） */
  defaultWhisperModelName: string;
  defaultTranslateModelName: string;

  // ---- SRT 翻译页面状态 ----
  srtSourceLanguage: string;
  srtTargetLanguage: string;
  srtTranslateModel: string;
  srtSegments: import('../types').SrtSegment[];
  srtTranslatedSegments: import('../types').SrtSegment[];
  srtTranslateStatus: 'idle' | 'translating' | 'done' | 'error' | 'stopped';
  srtError?: string;
  srtTranslateStartTime: number;

  // ---- 计算属性 ----
  getStats: () => QueueStats;
  getTotalDuration: () => number;
  getEstimatedRemaining: () => number;
  getFilteredTasks: (filter: string) => TranscriptionTask[];
  getSelectedTask: () => TranscriptionTask | undefined;

  // ---- 设置操作 ----
  updateSettings: (partial: Partial<AppSettings>) => void;

  // ---- 任务操作 ----
  addTask: (file: File) => void;
  addTaskByPath: (filePath: string) => void;
  removeTask: (id: string) => void;
  cancelTask: (id: string) => void;
  retryTask: (id: string) => void;
  clearCompleted: () => void;
  selectTask: (id: string | null) => void;

  // ---- 翻译操作 ----
  translateTask: (id: string) => void;

  // ---- SRT 翻译操作 ----
  setCurrentPage: (page: PageName) => void;
  setSrtSourceLanguage: (lang: string) => void;
  setSrtTargetLanguage: (lang: string) => void;
  setSrtTranslateModel: (model: string) => void;
  loadSrtFile: (file: File) => Promise<void>;
  translateSrt: () => Promise<void>;
  stopTranslateSrt: () => void;
  exportSrtOriginal: () => void;
  exportSrtTranslated: () => void;
  exportSrtBilingual: () => void;

  // ---- 后端状态 ----
  checkBackend: () => void;
}

/**
 * 清除某个任务的轮询定时器。
 */
function clearPollingTimer(id: string): void {
  const timer = pollingTimers.get(id);
  if (timer) {
    clearInterval(timer);
    pollingTimers.delete(id);
  }
}

/**
 * 启动轮询后端任务状态。
 */
function startPolling(
  taskId: string,
  backendTaskId: string,
  set: (fn: (state: QueueStore) => Partial<QueueStore>) => void,
  get: () => QueueStore,
): void {
  clearPollingTimer(taskId);

  const timer = setInterval(async () => {
    const state = get();
    const task = state.tasks.find((t) => t.id === taskId);
    if (!task || task.status === 'cancelled' || task.status === 'completed' || task.status === 'failed') {
      clearPollingTimer(taskId);
      return;
    }

    try {
      const result = await apiGetTaskStatus(state.settings.apiBaseUrl, backendTaskId);

      // 映射后端状态到前端状态
      const statusMap: Record<string, TaskStatus> = {
        queued: 'queued',
        loading: 'loading',
        transcribing: 'transcribing',
        completed: 'completed',
        failed: 'failed',
        cancelled: 'cancelled',
      };
      const newStatus = statusMap[result.status] || 'queued';

      // 更新任务
      set((s) => ({
        tasks: s.tasks.map((t) =>
          t.id === taskId
            ? {
                ...t,
                status: newStatus,
                progress: result.progress,
                currentChunk: result.current_chunk,
                totalChunks: result.total_chunks,
                skippedChunks: result.skipped_chunks,
                skippedChunkIndexes: result.skipped_chunk_indexes,
                segments: result.segments || [],
                duration: result.duration || t.duration,
                error: result.error || undefined,
                completedAt: result.completed_at ? result.completed_at * 1000 : undefined,
              }
            : t,
        ),
      }));

      // 如果完成或失败，停止轮询
      if (newStatus === 'completed' || newStatus === 'failed') {
        clearPollingTimer(taskId);
        // 自动选中新完成的任务
        if (newStatus === 'completed') {
          set((_s) => ({ selectedTaskId: taskId }));
        }
        // 自动启动下一个
        autoStartNext(set, get);
      }
    } catch (err) {
      console.error(`Polling error for task ${taskId}:`, err);
    }
  }, POLL_INTERVAL);

  pollingTimers.set(taskId, timer);
}

/**
 * 启动真实转录流程：上传文件 → 调用后端 → 轮询进度。
 */
async function startRealTranscription(
  id: string,
  filePath: string,
  set: (fn: (state: QueueStore) => Partial<QueueStore>) => void,
  get: () => QueueStore,
): Promise<void> {
  const state = get();
  const task = state.tasks.find((t) => t.id === id);
  if (!task) return;

  try {
    // 调用后端启动转录
    const result = await apiStartTranscription(
      state.settings.apiBaseUrl,
      filePath,
      state.settings.modelPath || undefined,
      task.language,
      task.chunkSec,
      task.overlapSec,
    );

    // 更新状态为 loading
    set((s) => ({
      tasks: s.tasks.map((t) =>
        t.id === id
          ? { ...t, status: 'loading' as TaskStatus, backendTaskId: result.task_id }
          : t,
      ),
    }));

    // 启动轮询
    startPolling(id, result.task_id, set, get);
  } catch (err: any) {
    console.error('Failed to start transcription:', err);
    set((s) => ({
      tasks: s.tasks.map((t) =>
        t.id === id
          ? { ...t, status: 'failed' as TaskStatus, error: err.message || '启动转录失败' }
          : t,
      ),
    }));
    autoStartNext(set, get);
  }
}

/**
 * 自动启动下一个排队中的任务。
 */
function autoStartNext(
  set: (fn: (state: QueueStore) => Partial<QueueStore>) => void,
  get: () => QueueStore,
): void {
  const state = get();
  const activeCount = state.tasks.filter(
    (t) => t.status === 'loading' || t.status === 'transcribing',
  ).length;
  const maxConcurrent = state.settings.maxConcurrent;

  if (activeCount < maxConcurrent) {
    const nextTask = state.tasks.find((t) => t.status === 'queued');
    if (nextTask && nextTask.filePath) {
      startRealTranscription(nextTask.id, nextTask.filePath, set, get);
    }
  }
}

export const useQueueStore = create<QueueStore>((set, get) => ({
  currentPage: 'transcribe',
  tasks: [],
  selectedTaskId: null,
  backendConnected: false,
  defaultWhisperModelName: '',
  defaultTranslateModelName: '',

  // SRT 翻译初始状态
  srtSourceLanguage: 'ja',
  srtTargetLanguage: 'zh',
  srtTranslateModel: '',
  srtSegments: [],
  srtTranslatedSegments: [],
  srtTranslateStatus: 'idle',
  srtError: undefined,
  srtTranslateStartTime: 0,

  settings: {
    modelPath: '',
    defaultLanguage: 'ja',
    defaultChunkSec: 150,
    defaultOverlapSec: 20,
    outputDir: '~/Downloads/srt_output',
    maxConcurrent: 1,
    apiBaseUrl: 'http://localhost:8765',
    translateModel: '',
  },

  getStats: () => {
    const tasks = get().tasks;
    return {
      total: tasks.length,
      queued: tasks.filter((t) => t.status === 'queued').length,
      loading: tasks.filter((t) => t.status === 'loading').length,
      transcribing: tasks.filter((t) => t.status === 'transcribing').length,
      completed: tasks.filter((t) => t.status === 'completed').length,
      failed: tasks.filter((t) => t.status === 'failed').length,
      cancelled: tasks.filter((t) => t.status === 'cancelled').length,
    };
  },

  getTotalDuration: () => {
    return get().tasks.reduce((sum, t) => sum + (t.duration ?? 0), 0);
  },

  getEstimatedRemaining: () => {
    const state = get();
    const activeTasks = state.tasks.filter(
      (t) => t.status === 'loading' || t.status === 'transcribing' || t.status === 'queued',
    );
    let totalSec = 0;
    for (const t of activeTasks) {
      const remaining = t.totalChunks - t.currentChunk;
      const effectiveChunk = t.chunkSec - t.overlapSec;
      totalSec += remaining * Math.max(effectiveChunk * 0.1, t.chunkSec * 0.15);
    }
    return Math.round(totalSec);
  },

  getFilteredTasks: (filter: string) => {
    const tasks = get().tasks;
    const sorted = [...tasks].sort((a, b) => a.createdAt - b.createdAt);
    switch (filter) {
      case 'transcribing':
        return sorted.filter(
          (t) => t.status === 'loading' || t.status === 'transcribing',
        );
      case 'completed':
        return sorted.filter((t) => t.status === 'completed');
      case 'failed':
        return sorted.filter((t) => t.status === 'failed');
      default:
        return sorted;
    }
  },

  getSelectedTask: () => {
    const state = get();
    if (!state.selectedTaskId) return undefined;
    return state.tasks.find((t) => t.id === state.selectedTaskId);
  },

  updateSettings: (partial: Partial<AppSettings>) => {
    set((state) => ({
      settings: { ...state.settings, ...partial },
    }));
  },

  addTask: async (file: File) => {
    const settings = get().settings;
    const modelName = getShortModelName(settings.modelPath);

    const newTask: TranscriptionTask = {
      id: generateId(),
      fileName: file.name,
      fileSize: file.size,
      filePath: '', // 先设为空，上传后更新
      language: settings.defaultLanguage,
      model: modelName,
      chunkSec: settings.defaultChunkSec,
      overlapSec: settings.defaultOverlapSec,
      status: 'queued',
      progress: 0,
      currentChunk: 0,
      totalChunks: 0,
      skippedChunks: 0,
      skippedChunkIndexes: [],
      segments: [],
      translatedSegments: [],
      translationStatus: 'idle',
      createdAt: Date.now(),
    };

    set((state) => ({ tasks: [...state.tasks, newTask] }));

    // 上传文件到后端
    try {
      const uploadResult = await apiUploadFile(settings.apiBaseUrl, file);
      // 更新文件路径
      set((state) => ({
        tasks: state.tasks.map((t) =>
          t.id === newTask.id ? { ...t, filePath: uploadResult.file_path } : t,
        ),
      }));
      autoStartNext(set, get);
    } catch (err: any) {
      set((state) => ({
        tasks: state.tasks.map((t) =>
          t.id === newTask.id
            ? { ...t, status: 'failed' as TaskStatus, error: `上传失败: ${err.message}` }
            : t,
        ),
      }));
    }
  },

  addTaskByPath: (filePath: string) => {
    const settings = get().settings;
    const modelName = getShortModelName(settings.modelPath);

    const newTask: TranscriptionTask = {
      id: generateId(),
      fileName: filePath.split('/').pop() || filePath,
      fileSize: 0,
      filePath,
      language: settings.defaultLanguage,
      model: modelName,
      chunkSec: settings.defaultChunkSec,
      overlapSec: settings.defaultOverlapSec,
      status: 'queued',
      progress: 0,
      currentChunk: 0,
      totalChunks: 0,
      skippedChunks: 0,
      skippedChunkIndexes: [],
      segments: [],
      translatedSegments: [],
      translationStatus: 'idle',
      createdAt: Date.now(),
    };

    set((state) => ({ tasks: [...state.tasks, newTask] }));
    autoStartNext(set, get);
  },

  removeTask: (id: string) => {
    clearPollingTimer(id);
    set((state) => ({
      tasks: state.tasks.filter((t) => t.id !== id),
      selectedTaskId: state.selectedTaskId === id ? null : state.selectedTaskId,
    }));
  },

  cancelTask: (id: string) => {
    clearPollingTimer(id);
    const task = get().tasks.find((t) => t.id === id);
    if (task?.backendTaskId) {
      apiCancelTask(get().settings.apiBaseUrl, task.backendTaskId).catch(console.error);
    }
    set((state) => ({
      tasks: state.tasks.map((t) =>
        t.id === id ? { ...t, status: 'cancelled' as TaskStatus } : t,
      ),
    }));
  },

  retryTask: (id: string) => {
    clearPollingTimer(id);
    set((state) => ({
      tasks: state.tasks.map((t) =>
        t.id === id
          ? {
              ...t,
              status: 'queued' as TaskStatus,
              progress: 0,
              currentChunk: 0,
              skippedChunks: 0,
              skippedChunkIndexes: [],
              segments: [],
              translatedSegments: [],
              translationStatus: 'idle' as const,
              error: undefined,
              completedAt: undefined,
              outputSrtPath: undefined,
            }
          : t,
      ),
    }));
    autoStartNext(set, get);
  },

  clearCompleted: () => {
    const toClear = get().tasks.filter(
      (t) => t.status === 'completed' || t.status === 'cancelled',
    );
    toClear.forEach((t) => clearPollingTimer(t.id));
    const isSelectedCleared = toClear.some((t) => t.id === get().selectedTaskId);
    set((state) => ({
      tasks: state.tasks.filter(
        (t) => t.status !== 'completed' && t.status !== 'cancelled',
      ),
      selectedTaskId: isSelectedCleared ? null : state.selectedTaskId,
    }));
  },

  selectTask: (id: string | null) => {
    set({ selectedTaskId: id });
  },

  translateTask: async (id: string) => {
    const task = get().tasks.find((t) => t.id === id);
    if (!task || task.segments.length === 0) return;

    // 标记翻译中
    set((state) => ({
      tasks: state.tasks.map((t) =>
        t.id === id ? { ...t, translationStatus: 'translating' as const } : t,
      ),
    }));

    try {
      const translatedSegments = await apiTranslate(
        get().settings.apiBaseUrl,
        task.segments,
        task.language,
        'zh',
        get().settings.translateModel || undefined,
      );
      set((state) => ({
        tasks: state.tasks.map((t) =>
          t.id === id
            ? {
                ...t,
                translatedSegments,
                translationStatus: 'done' as const,
              }
            : t,
        ),
      }));
    } catch (err: any) {
      console.error('Translation failed:', err);
      set((state) => ({
        tasks: state.tasks.map((t) =>
          t.id === id
            ? {
                ...t,
                translationStatus: 'idle' as const,
                error: `翻译失败: ${err.message}`,
              }
            : t,
        ),
      }));
    }
  },

  checkBackend: async () => {
    try {
      const { apiHealthCheck } = await import('../utils/helpers');
      const result = await apiHealthCheck(get().settings.apiBaseUrl);
      const whisperName = result.whisper_model
        ? result.whisper_model.split('/').pop() || ''
        : '';
      const translateName = result.translate_model
        ? result.translate_model.split('/').pop() || ''
        : '';
      set({
        backendConnected: result.status === 'ok',
        defaultWhisperModelName: whisperName,
        defaultTranslateModelName: translateName,
      });
    } catch {
      set({ backendConnected: false });
    }
  },

  // ---- SRT 翻译操作 ----

  setCurrentPage: (page: import('../types').PageName) => {
    set({ currentPage: page });
  },

  setSrtSourceLanguage: (lang: string) => {
    set({ srtSourceLanguage: lang });
  },

  setSrtTargetLanguage: (lang: string) => {
    set({ srtTargetLanguage: lang });
  },

  setSrtTranslateModel: (model: string) => {
    set({ srtTranslateModel: model });
  },

  loadSrtFile: async (file: File) => {
    try {
      const text = await file.text();
      const segments = parseSrt(text);
      set({
        srtSegments: segments,
        srtTranslatedSegments: [],
        srtTranslateStatus: 'idle',
        srtError: undefined,
      });
    } catch (err: any) {
      set({
        srtTranslateStatus: 'error',
        srtError: `加载 SRT 失败: ${err.message}`,
      });
    }
  },

  translateSrt: async () => {
    const state = get();
    if (state.srtSegments.length === 0) return;

    const isResume = state.srtTranslateStatus === 'stopped';
    const startIdx = isResume ? state.srtTranslatedSegments.length : 0;

    // 批量翻译：每批 15 段一起发送，让 LLM 看到上下文，同时减少 HTTP 往返
    const BATCH_SIZE = 15;

    // 创建新的 AbortController
    srtAbortController = new AbortController();
    const { signal } = srtAbortController;

    set({
      srtTranslateStatus: 'translating',
      srtError: undefined,
      srtTranslatedSegments: isResume ? state.srtTranslatedSegments : [],
      srtTranslateStartTime: Date.now(),
    });

    const translated: import('../types').SrtSegment[] = isResume ? [...state.srtTranslatedSegments] : [];
    let hasError = false;
    let stopped = false;

    /**
     * 压缩翻译结果中的重复字符/词语。
     * 单字：「哈哈哈哈哈哈」→「哈～」
     * 多字词：「算了，算了，算了」→「算了～」
     * 规则：去除标点后，同一个单元（1-4 字）重复 3 次以上即压缩
     */
    const compressRepeated = (text: string): string => {
      if (!text || text.length < 3) return text;

      // 去除常见分隔符，提取纯文本
      const stripped = text.replace(/[，。！？、；：\s,!.?;:　]+/g, '');
      if (stripped.length < 3) return text;

      // 尝试不同单元长度（从 4 字到 1 字），找到最长可重复单元
      for (let unitLen = Math.min(4, Math.floor(stripped.length / 3)); unitLen >= 1; unitLen--) {
        if (stripped.length % unitLen !== 0) continue;
        const unit = stripped.substring(0, unitLen);
        const repeatCount = stripped.length / unitLen;
        if (unit.repeat(repeatCount) === stripped && repeatCount >= 3) {
          return unit + '～';
        }
      }
      return text;
    };

    for (let i = startIdx; i < state.srtSegments.length; i += BATCH_SIZE) {
      // 检查是否被停止
      if (signal.aborted) {
        stopped = true;
        break;
      }

      const batch = state.srtSegments.slice(i, Math.min(i + BATCH_SIZE, state.srtSegments.length));
      try {
        const results = await apiTranslate(
          state.settings.apiBaseUrl,
          batch,
          state.srtSourceLanguage,
          state.srtTargetLanguage,
          state.srtTranslateModel || undefined,
        );
        // 逐条匹配：后端按顺序返回，数量和输入一致
        for (let j = 0; j < batch.length; j++) {
          if (j < results.length) {
            translated.push({
              ...results[j],
              translatedText: compressRepeated(results[j].translatedText || ''),
            });
          } else {
            // 行数不匹配时回退原文
            translated.push({ ...batch[j], translatedText: batch[j].text });
          }
        }
      } catch (err: any) {
        console.error(`SRT batch translate failed at index ${i}-${i + batch.length - 1}:`, err);
        hasError = true;
        // 整批失败，全部保留原文
        for (const seg of batch) {
          translated.push({ ...seg, translatedText: seg.text });
        }
      }
      // 每批完成更新一次 UI
      set({ srtTranslatedSegments: [...translated] });
    }

    srtAbortController = null;

    if (stopped) {
      set({ srtTranslateStatus: 'stopped', srtTranslateStartTime: 0 });
      return;
    }

    if (hasError) {
      set({
        srtTranslateStatus: 'error',
        srtError: '部分段落翻译失败，已保留原文',
        srtTranslateStartTime: 0,
      });
    } else {
      set({ srtTranslateStatus: 'done', srtTranslateStartTime: 0 });
    }
  },

  stopTranslateSrt: () => {
    if (srtAbortController) {
      srtAbortController.abort();
      srtAbortController = null;
    }
  },

  exportSrtOriginal: () => {
    const state = get();
    if (state.srtSegments.length === 0) return;
    const srtContent = exportSegmentsToSrt(state.srtSegments, false);
    downloadSrt(srtContent, 'original.srt');
  },

  exportSrtTranslated: () => {
    const state = get();
    if (state.srtTranslatedSegments.length === 0) return;
    const srtContent = exportSegmentsToSrt(state.srtTranslatedSegments, true);
    downloadSrt(srtContent, 'translated.srt');
  },

  exportSrtBilingual: () => {
    const state = get();
    if (state.srtSegments.length === 0) return;
    const bilingual = state.srtSegments.map((seg, i) => {
      const translated = state.srtTranslatedSegments[i]?.translatedText || '';
      return [
        seg.index,
        `${formatSrtTime(seg.startTime)} --> ${formatSrtTime(seg.endTime)}`,
        seg.text,
        '',
        translated,
      ].join('\n');
    }).join('\n\n');
    downloadSrt(bilingual, 'bilingual.srt');
  },
}));

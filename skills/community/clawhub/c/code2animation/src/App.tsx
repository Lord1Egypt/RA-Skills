import { useState, useEffect, useRef, useMemo } from 'react';
import PlaybackControls from './components/PlaybackControls';
import { Player } from './components/Player';
import { useTTS } from './hooks/useTTS';
import { useProject } from './hooks/useProject';
import { usePlayback } from './hooks/usePlayback';
import { VideoClip } from '@/types';

import { generateAudio, loadAudioFiles, checkAudioExists, getSpeechClips } from './utils/audioManager';
import { 
  calculateCompleteTimeline, 
  calculateEstimatedTimeline, 
  getCurrentMediaFromTimeline, 
  getClipPositionFromGlobalTime,
  getGlobalTimeFromClipPosition,
  seekToTime,
  PlaybackTimeline 
} from './utils/playbackEngine';
import { getActiveMediaStates } from '@/utils/transitionEngine';

export default function App() {
  const [audioCache, setAudioCache] = useState<Map<string, HTMLAudioElement>>(new Map());
  const [isLoadingAudio, setIsLoadingAudio] = useState(false);
  const [currentWord, setCurrentWord] = useState<string>('');
  const [mediaItems, setMediaItems] = useState<any[]>([]);
  const [timeline, setTimeline] = useState<PlaybackTimeline | null>(null);
  const [audioInitialized, setAudioInitialized] = useState(false);
  const [iframesLoaded, setIframesLoaded] = useState(0);

  // Check for render mode from URL params
  const urlParams = new URLSearchParams(window.location.search);
  const isRecordMode = urlParams.get('record') === 'true';
  const urlOrientation = urlParams.get('orientation');
  const urlProject = urlParams.get('project');

  // Override defaults if in record mode
  const initialProject = urlProject || 'agentSaasPromoVideo';
  const initialPortrait = urlOrientation === 'portrait';

  // Use custom hooks
  const { projects, availableProjects, activeProject, setActiveProject, isLoadingProject, currentProject } = useProject(initialProject);

  const [configError, setConfigError] = useState<string | null>(null);

  // Calculate complete timeline once
  useEffect(() => {
    if (!currentProject) {
      setTimeline(null);
      setMediaItems([]);
      return;
    }

    try {
      setConfigError(null);
      
      // First, create estimated timeline for immediate use
      const estimatedTimeline = calculateEstimatedTimeline(currentProject);
      setTimeline(estimatedTimeline);
      setMediaItems(estimatedTimeline.mediaItems);
      console.log('[Timeline] Estimated timeline ready:', estimatedTimeline);
      
      // Then, calculate accurate timeline with word boundaries
      calculateCompleteTimeline(currentProject).then(accurateTimeline => {
        setTimeline(accurateTimeline);
        setMediaItems(accurateTimeline.mediaItems);
        console.log('[Timeline] Accurate timeline ready:', accurateTimeline);
      }).catch(error => {
        console.warn('[Timeline] Failed to load accurate timeline, using estimates:', error);
      });
    } catch (error: any) {
      setConfigError(error.message || 'Failed to process project');
      console.error('[Config Error]', error);
      setTimeline(null);
      setMediaItems([]);
    }
  }, [currentProject]);

  const processedClips = useMemo(() => {
    return currentProject?.clips || [];
  }, [currentProject]);

  const [isPortrait, setIsPortrait] = useState(initialPortrait);

  const {
    currentClipIndex,
    setCurrentClipIndex,
    currentTime,
    setCurrentTime,
    isPlaying,
    setIsPlaying,
    resetCounter,
    nextClip,
    prevClip,
    reset
  } = usePlayback(processedClips);

  useEffect(() => {
    if (urlProject && urlProject !== activeProject) {
      setActiveProject(urlProject);
    }
  }, [urlProject, activeProject, setActiveProject]);

  // In record mode, auto-initialize audio state so renderState computes properly
  useEffect(() => {
    if (isRecordMode && !audioInitialized) {
      setAudioInitialized(true);
    }
  }, [isRecordMode, audioInitialized]);

  // TTS Integration - use preloaded audio from cache
  const currentClip = processedClips[currentClipIndex] as VideoClip;
  const shouldUseTTS = currentClip?.type !== 'transition' && currentClip?.speech;

  // Calculate the audio file index by counting non-transition clips up to and including current
  const audioClipIndex = shouldUseTTS
    ? processedClips.slice(0, currentClipIndex + 1).filter(c => c.type !== 'transition').length - 1
    : undefined;

  // Get preloaded audio from cache
  const cachedAudio = audioClipIndex !== undefined
    ? audioCache.get(`${activeProject}-${audioClipIndex}`)
    : undefined;

  const {
    isLoading: isTTSLoading,
    speak,
    pause: pauseTTS,
    resume: resumeTTS,
    stop: stopTTS,
    duration: ttsDuration
  } = useTTS({
    clip: shouldUseTTS ? currentClip : undefined,
    projectId: shouldUseTTS ? activeProject : undefined,
    clipIndex: audioClipIndex,
    preloadedAudio: cachedAudio,
    onWordBoundary: (word) => {
      console.log('[TTS] Word boundary:', word);
      setCurrentWord(word);
    },
    onEnd: () => {
      console.log('[TTS] Audio ended');
      // Don't auto-advance here, let the normal clip timing handle it
    }
  });

  const containerRef = useRef<HTMLDivElement>(null);
  const [scale, setScale] = useState(1);

  const CANVAS_WIDTH = isPortrait ? 1080 : 1920;
  const CANVAS_HEIGHT = isPortrait ? 1920 : 1080;

  const clipDuration = useMemo(() => {
    if (!timeline || currentClipIndex >= timeline.clipDurations.length) return 4;
    return timeline.clipDurations[currentClipIndex];
  }, [timeline, currentClipIndex]);

  const globalPlaybackTime = useMemo(() => {
    if (!timeline) return 0;
    return getGlobalTimeFromClipPosition(timeline, currentClipIndex, currentTime);
  }, [timeline, currentClipIndex, currentTime]);

  useEffect(() => {
    const updateScale = () => {
      if (containerRef.current) {
        const { clientWidth, clientHeight } = containerRef.current;
        const availableWidth = clientWidth - 64; // 32px padding on each side
        const availableHeight = clientHeight - 64;

        const scaleX = availableWidth / CANVAS_WIDTH;
        const scaleY = availableHeight / CANVAS_HEIGHT;
        setScale(Math.min(scaleX, scaleY));
      }
    };

    updateScale();
    window.addEventListener('resize', updateScale);
    return () => window.removeEventListener('resize', updateScale);
  }, [isPortrait, CANVAS_WIDTH, CANVAS_HEIGHT]);

  // Handle clip advancement
  useEffect(() => {
    if (currentTime >= clipDuration && isPlaying) {
      if (currentClipIndex < processedClips.length - 1) {
        const nextIndex = currentClipIndex + 1;
        setCurrentClipIndex(nextIndex);
        setCurrentTime(0);
        setCurrentWord(''); // Reset word on clip change
      } else {
        setIsPlaying(false);
        setCurrentTime(clipDuration);
      }
    }
  }, [currentTime, clipDuration, isPlaying, currentClipIndex, processedClips, setCurrentClipIndex, setCurrentTime, setIsPlaying]);

  // Auto-start TTS when clip changes and is playing (only if audio is initialized)
  useEffect(() => {
    if (isPlaying && shouldUseTTS && currentTime === 0 && audioInitialized) {
      speak();
    }
  }, [currentClipIndex, shouldUseTTS, isPlaying, speak, currentTime, audioInitialized]);

  // Sync time with all iframes
  useEffect(() => {
    const syncWithIframes = () => {
      const iframes = document.querySelectorAll('iframe');
      iframes.forEach(iframe => {
        if (iframe.contentWindow) {
          try {
            iframe.contentWindow.postMessage({
              type: 'seek',
              time: currentTime,
              globalTime: globalPlaybackTime
            }, '*');
          } catch (e) {
            // Ignore cross-origin errors
          }
        }
      });
    };

    // Sync when time changes and we're playing, or when iframes are loaded
    if (isPlaying || currentTime > 0 || iframesLoaded > 0) {
      syncWithIframes();
    }
  }, [currentTime, globalPlaybackTime, isPlaying, iframesLoaded]);

  const handleIframeLoad = () => {
    setIframesLoaded(prev => prev + 1);
    // Sync current time with newly loaded iframe
    setTimeout(() => {
      const iframes = document.querySelectorAll('iframe');
      iframes.forEach(iframe => {
        if (iframe.contentWindow) {
          try {
            iframe.contentWindow.postMessage({
              type: 'seek',
              time: currentTime,
              globalTime: globalPlaybackTime
            }, '*');
          } catch (e) {
            // Ignore cross-origin errors
          }
          }
        });
      }, 100); // Small delay to ensure iframe script is loaded
  };

  const togglePlay = async () => {
    console.log('[togglePlay] Function called, isPlaying:', isPlaying);

    // If trying to play and audio not initialized, handle audio loading/generation
    if (!isPlaying && !audioInitialized) {
      console.log('[togglePlay] Starting audio loading process...');
      setIsLoadingAudio(true);

      try {
        const speechClips = getSpeechClips(currentProject);
        console.log('[togglePlay] Found', speechClips.length, 'speech clips');
        console.log('[togglePlay] Speech clips:', speechClips.map((c: VideoClip) => c.speech?.substring(0, 30)));

        if (speechClips.length > 0) {
          // Check if audio files exist
          console.log('[togglePlay] Checking if audio exists for project:', activeProject);
          const audioExists = await checkAudioExists(activeProject, speechClips);
          console.log('[togglePlay] Audio exists:', audioExists);

          if (!audioExists) {
            console.log(`[togglePlay] Audio missing, calling generateAudio API...`);

            const result = await generateAudio(activeProject);
            console.log('[togglePlay] Generate audio result:', result);

            if (!result.success) {
              throw new Error(result.error || 'Audio generation failed');
            }

            console.log('[togglePlay] Audio generation successful:', result.message);
          } else {
            console.log('[togglePlay] Audio files already exist, skipping generation');
          }

          // Now load all audio files
          console.log('[togglePlay] Loading audio files...');
          const newCache = await loadAudioFiles(activeProject, speechClips);
          setAudioCache(newCache);
          console.log(`[togglePlay] Successfully loaded ${newCache.size} audio files`);
        } else {
          console.log('[togglePlay] No speech clips found, skipping audio processing');
        }

        setAudioInitialized(true);
        setIsLoadingAudio(false);
      } catch (error: any) {
        console.error('[togglePlay] Audio loading failed:', error);
        alert(`Failed to load audio: ${error.message}`);
        setIsLoadingAudio(false);
        return;
      }
    }

    if (currentTime >= clipDuration && currentClipIndex >= processedClips.length - 1) {
      setCurrentClipIndex(0);
      setCurrentTime(0);
    }

    const newIsPlaying = !isPlaying;
    console.log('[togglePlay] Setting isPlaying to:', newIsPlaying);
    setIsPlaying(newIsPlaying);

    // Sync TTS audio
    if (shouldUseTTS && audioInitialized) {
      if (newIsPlaying) {
        if (currentTime === 0) {
          speak(); // Start from beginning
        } else {
          resumeTTS(); // Resume from current position
        }
      } else {
        pauseTTS();
      }
    }
  };

  const handleNextClip = () => {
    stopTTS(); // Stop current TTS
    setCurrentWord(''); // Reset word
    nextClip();
  };

  const handlePrevClip = () => {
    stopTTS(); // Stop current TTS
    setCurrentWord(''); // Reset word
    prevClip();
  };

  const handleReset = () => {
    stopTTS(); // Stop current TTS
    setCurrentWord(''); // Reset word
    setAudioInitialized(false); // Reset to uninitialized state
    setAudioCache(new Map()); // Clear audio cache
    setIframesLoaded(0); // Reset iframe counter
    reset();
  };

  const toggleOrientation = () => {
    setIsPortrait(!isPortrait);
  };

  // 使用预计算的时间轴渲染状态
  const renderState = useMemo(() => {
    if (!timeline) {
      return { activeMedias: [], currentClip: null };
    }

    const activeMedias = getActiveMediaStates(timeline, globalPlaybackTime);
    let mediasToRender = activeMedias;

    if (mediasToRender.length === 0) {
      const fallbackMedia = getCurrentMediaFromTimeline(timeline, globalPlaybackTime);
      if (fallbackMedia) {
        mediasToRender = [{ media: fallbackMedia, style: { opacity: 1, transform: 'translate3d(0, 0, 0)', zIndex: 1 } }];
      }
    }

    if (mediasToRender[0]?.media) {
      const firstMedia = mediasToRender[0].media;
      console.log(`[Render] Global time ${globalPlaybackTime.toFixed(2)}s, Media: ${firstMedia.src.split('/').pop()}, Words: "${firstMedia.words}"`);
    }

    return {
      activeMedias: mediasToRender,
      currentClip: processedClips[currentClipIndex] || null,
      timeline // Pass timeline to Player
    };
  }, [timeline, globalPlaybackTime, processedClips, currentClipIndex]);

  // Expose functions for rendering mode
  useEffect(() => {
    if (isRecordMode && timeline) {
      // Get total duration using timeline
      const getTotalDurationFunc = () => {
        return timeline.totalDuration;
      };

      // Seek to specific time using timeline
      const seekTo = (time: number) => {
        const position = seekToTime(timeline, time);
        setCurrentClipIndex(position.clipIndex);
        setCurrentTime(position.localTime);
        setIsPlaying(false);
      };

      // Get audio log with timings from timeline
      const getAudioLog = () => {
        let accumulated = 0;
        return timeline.clipDurations.map((duration, index) => {
          const result = {
            file: `${activeProject}/audio/${index}.mp3`,
            startTime: accumulated
          };
          accumulated += duration;
          return result;
        });
      };

      // Get current clip index
      const getCurrentClipIndex = () => {
        return currentClipIndex;
      };

      // Expose to window for puppeteer
      (window as any).seekTo = seekTo;
      (window as any).getTotalDuration = getTotalDurationFunc;
      (window as any).getAudioLog = getAudioLog;
      (window as any).getCurrentClipIndex = getCurrentClipIndex;
      (window as any).suppressTTS = true;

      console.log('[Render Mode] Functions exposed to window');
    }
  }, [isRecordMode, timeline, activeProject, currentClipIndex]);

  if (isLoadingProject || !currentProject) {
    return (
      <div className="min-h-screen bg-neutral-950 text-white flex items-center justify-center">
        <div className="animate-pulse">Loading project...</div>
      </div>
    );
  }

  if (configError) {
    return (
      <div className="min-h-screen bg-neutral-950 text-white flex items-center justify-center p-8">
        <div className="max-w-2xl">
          <div className="bg-red-900/20 border border-red-500 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-red-400 mb-4">Configuration Error</h2>
            <p className="text-red-200 mb-4 whitespace-pre-wrap">{configError}</p>
            <button
              onClick={() => {
                setConfigError(null);
                window.location.reload();
              }}
              className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded transition-colors"
            >
              Reload
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`h-screen w-screen bg-neutral-950 text-white flex flex-col font-sans overflow-hidden ${isRecordMode && !isLoadingAudio ? 'ready-to-record' : ''}`}>
      {/* Main Canvas Area */}
      <main ref={containerRef} className="flex-1 relative flex items-center justify-center bg-[#0a0a0a] overflow-hidden">
        <div
          className="relative bg-black shadow-2xl ring-1 ring-neutral-800 overflow-hidden shrink-0"
          style={{
            width: CANVAS_WIDTH,
            height: CANVAS_HEIGHT,
            transform: `scale(${scale})`,
            transformOrigin: 'center center'
          }}
        >
          <Player renderState={renderState} background={currentProject.background} resetCounter={resetCounter} isPlaying={isPlaying} onIframeLoad={handleIframeLoad} />
        </div>
      </main>

      {/* Bottom Controls Bar */}
      {!isRecordMode && (
        <PlaybackControls
          projects={projects}
          availableProjects={availableProjects}
          activeProject={activeProject}
          isGenerating={isTTSLoading}
          isLoadingAudio={isLoadingAudio}
          isPlaying={isPlaying}
          currentClipIndex={currentClipIndex}
          currentTime={currentTime}
          clipDuration={clipDuration}
          totalClips={currentProject.clips.length}
          isPortrait={isPortrait}
          onProjectChange={(projectId: string) => {
            stopTTS(); // Stop current TTS when switching projects
            setCurrentWord(''); // Reset word
            setActiveProject(projectId);
            setCurrentClipIndex(0);
            setCurrentTime(0);
            setIsPlaying(false);
            setAudioInitialized(false); // Reset audio initialization
            setAudioCache(new Map()); // Clear audio cache
            setIframesLoaded(0); // Reset iframe counter
          }}
          onTogglePlay={togglePlay}
          onNextClip={handleNextClip}
          onPrevClip={handlePrevClip}
          onReset={handleReset}
          onToggleOrientation={toggleOrientation}
        />
      )}
    </div>
  );
}

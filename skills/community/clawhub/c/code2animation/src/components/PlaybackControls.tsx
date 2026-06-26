import React from 'react';
import { Play, Pause, Monitor, Smartphone, SkipForward, SkipBack, RotateCcw } from 'lucide-react';

interface ProjectInfo {
  id: string;
  name: string;
  description?: string;
}

interface PlaybackControlsProps {
  // Project and state
  projects: Record<string, any>;
  availableProjects: ProjectInfo[];
  activeProject: string;
  isGenerating: boolean;
  isLoadingAudio: boolean;
  
  // Playback state
  isPlaying: boolean;
  currentClipIndex: number;
  currentTime: number;
  clipDuration: number;
  totalClips: number;
  
  // UI state
  isPortrait: boolean;
  
  // Event handlers
  onProjectChange: (projectId: string) => void;
  onTogglePlay: () => Promise<void>;
  onNextClip: () => void;
  onPrevClip: () => void;
  onReset: () => void;
  onToggleOrientation: () => void;
}

export default function PlaybackControls({
  projects,
  availableProjects,
  activeProject,
  isGenerating,
  isLoadingAudio,
  isPlaying,
  currentClipIndex,
  currentTime,
  clipDuration,
  totalClips,
  isPortrait,
  onProjectChange,
  onTogglePlay,
  onNextClip,
  onPrevClip,
  onReset,
  onToggleOrientation
}: PlaybackControlsProps) {
  // Use availableProjects if available, otherwise fallback to loaded projects
  const projectList = availableProjects.length > 0 
    ? availableProjects 
    : Object.keys(projects).map(id => ({ id, name: id }));

  return (
    <div className="h-16 bg-zinc-900 border-t border-zinc-800 flex items-center px-6 justify-between w-full shrink-0">
      {/* Left Controls */}
      <div className="flex items-center space-x-4">
        <select
          value={activeProject}
          onChange={(e: React.ChangeEvent<HTMLSelectElement>) => {
            onProjectChange(e.target.value);
          }}
          className="bg-zinc-800 text-sm font-bold text-white border border-white/10 rounded px-2 py-1 cursor-pointer hover:border-[#00FF00] transition-colors outline-none"
        >
          {projectList.map(project => (
            <option key={project.id} value={project.id}>
              {project.name}
            </option>
          ))}
        </select>

        {(isGenerating || isLoadingAudio) && (
          <div className="flex items-center space-x-2 text-[#00FF00] text-xs">
            <div className="animate-spin w-3 h-3 border border-[#00FF00] border-t-transparent rounded-full"></div>
            <span>{isGenerating ? 'Generating Audio...' : 'Loading Audio...'}</span>
          </div>
        )}

        <button
          onClick={onToggleOrientation}
          className="p-2 rounded hover:bg-white/10 text-zinc-400 hover:text-white transition-colors"
          title={isPortrait ? "Switch to Landscape" : "Switch to Portrait"}
        >
          {isPortrait ? <Monitor size={18} /> : <Smartphone size={18} />}
        </button>
      </div>

      {/* Center Playback Controls */}
      <div className="flex items-center space-x-4 absolute left-1/2 transform -translate-x-1/2">
        <button 
          onClick={onPrevClip} 
          className="p-2 rounded-full hover:bg-white/10 text-zinc-400 hover:text-white transition-colors"
        >
          <SkipBack size={20} />
        </button>

        <button
          onClick={() => {
            console.log('[PlayButton] Button clicked!');
            if (!isLoadingAudio) {
              onTogglePlay();
            }
          }}
          disabled={isLoadingAudio}
          className={`flex items-center justify-center w-10 h-10 rounded-full transition-all ${
            isLoadingAudio 
              ? 'bg-gray-400 text-gray-600 cursor-not-allowed' 
              : 'bg-white text-black hover:bg-[#00FF00] hover:scale-105'
          }`}
        >
          {isLoadingAudio ? (
            <div className="animate-spin w-4 h-4 border-2 border-gray-600 border-t-transparent rounded-full"></div>
          ) : isPlaying ? (
            <Pause size={18} fill="currentColor" />
          ) : (
            <Play size={18} fill="currentColor" className="ml-1" />
          )}
        </button>

        <button 
          onClick={onNextClip} 
          className="p-2 rounded-full hover:bg-white/10 text-zinc-400 hover:text-white transition-colors"
        >
          <SkipForward size={20} />
        </button>
      </div>

      {/* Right Info & Reset */}
      <div className="flex items-center space-x-6">
        <div className="flex flex-col text-right">
          <span className="text-[10px] font-mono text-zinc-500 uppercase font-bold">
            Clip {currentClipIndex + 1}/{totalClips}
          </span>
          <span className="text-sm font-mono text-[#00FF00]">
            {currentTime.toFixed(2)}s / {clipDuration.toFixed(2)}s
          </span>
        </div>
        
        <button 
          onClick={onReset}
          className="px-4 py-1.5 bg-zinc-800 hover:bg-zinc-700 transition-colors rounded text-sm font-medium flex items-center gap-2 text-zinc-300 hover:text-white"
        >
          <RotateCcw size={14} /> Reset
        </button>
      </div>
    </div>
  );
}
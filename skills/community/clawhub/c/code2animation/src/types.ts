export interface AudioAlignment {
  characters: string[];
  character_start_times_seconds: number[];
  character_end_times_seconds: number[];
}

export type TransitionKind = 'fade' | 'zoom' | 'slide2Left' | 'slideUp' | 'none';

export interface MediaItem {
  src?: string;
  words?: string;
  type?: string;
  duration?: number;
  transitionIn?: TransitionKind;
  transitionDuration?: number;
  stayInClip?: boolean; // If true, media remains until clip end
  stay?: number; // Legacy support: number of switches to stay visible
}

export interface VideoClip {
  type: string;
  speech?: string;
  media?: MediaItem[];
  voice?: string;
  duration?: number;
}

export interface VideoProject {
  name: string;
  background?: string;
  clips: VideoClip[];
}

export interface WordBoundaryEvent {
  word: string;
  startTime: number;
  endTime: number;
}

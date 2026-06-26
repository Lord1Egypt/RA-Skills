export type TransitionKind = 'fade' | 'zoom' | 'slide2Left' | 'slideUp' | 'none';

export interface GlobalMediaEntry {
  id: string;
  duration: number;
  globalStartTime: number;
  transition2next?: TransitionKind;
  transitionDuration?: number;
  stayInClip?: boolean;
  stay?: number;
}

export interface TransitionStyle {
  opacity: string;
  transform: string;
  willChange: string;
  transition: 'none';
  zIndex?: number;
}

export interface TransitionState {
  isTransitioning: boolean;
  styles: Map<string, TransitionStyle>;
}

export interface TransitionPair {
  type: TransitionKind;
  outgoingId: string;
  incomingId: string;
  startTime: number;
  endTime: number;
  duration: number;
}

export declare function calculateTransitionState(
  mediaTimeline: GlobalMediaEntry[],
  globalTime: number
): TransitionState;

export declare function buildTransitionPairs(mediaTimeline: GlobalMediaEntry[]): TransitionPair[];

export declare function getTransitionGroups(mediaTimeline: GlobalMediaEntry[]): Map<string, TransitionPair[]>;

export declare class MediaTransitionManager {
  calculateTransitionStyles(mediaTimeline: GlobalMediaEntry[], globalTime: number): Map<string, TransitionStyle>;
  clearTransitions(): void;
}

export interface ActiveMediaState {
  media: GlobalMediaEntry;
  style: TransitionStyle;
}

export declare function getActiveMediaStates(
  mediaTimeline: GlobalMediaEntry[],
  globalTime: number
): ActiveMediaState[];

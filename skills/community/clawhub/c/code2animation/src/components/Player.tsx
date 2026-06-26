import { MediaRenderer } from './MediaRenderer';
import { DeterministicIframe } from './DeterministicIframe';

interface PlayerProps {
  renderState: any;
  background: string;
  resetCounter: number;
  isPlaying: boolean;
  onIframeLoad?: () => void;
}

export const Player = ({ renderState, background, resetCounter, isPlaying, onIframeLoad }: PlayerProps) => {
  if (!renderState || !renderState.activeMedias) return <div className="absolute inset-0 bg-black" />;
  const activeIds = new Set(
    renderState.activeMedias.map(({ media }: any) => media?.id).filter(Boolean)
  );
  const preloadMedias = (renderState.preloadMedias || []).filter((media: any) => !activeIds.has(media?.id));

  return (
    <div className="absolute inset-0 overflow-hidden bg-neutral-900" style={{ transition: 'none' }}>
      {/* Background */}
      <div className="absolute inset-0">
        {background && background.endsWith('.html') ? (
          <DeterministicIframe
            src={background}
            className="w-full h-full border-none"
            title="Background"
            onLoad={onIframeLoad}
          />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center opacity-30">
            <span className="text-neutral-500 font-mono text-lg">{background}</span>
          </div>
        )}
      </div>

      {/* Media Layer */}
      <div className="absolute inset-0">
        {preloadMedias.map((media: any, index: number) => (
          <MediaRenderer
            key={`preload-${media.id || index}`}
            media={media}
            style={{ opacity: 0, pointerEvents: 'none' }}
            isPlaying={isPlaying}
            onIframeLoad={onIframeLoad}
          />
        ))}

        {renderState.activeMedias.map(({ media, style }: any, index: number) => (
          <MediaRenderer
            key={media.id || `media-${index}`}
            media={media}
            style={style}
            isPlaying={isPlaying}
            onIframeLoad={onIframeLoad}
          />
        ))}
      </div>
    </div>
  );
};

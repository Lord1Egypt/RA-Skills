import "./index.css";
import { Composition } from "remotion";
import { ConversationVideo, totalDuration } from "./Conversation";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="Conversation"
      component={ConversationVideo}
      durationInFrames={totalDuration}
      fps={30}
      width={1280}
      height={720}
    />
  );
};

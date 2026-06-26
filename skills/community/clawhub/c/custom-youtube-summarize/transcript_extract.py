import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_PATH = os.path.join(BASE_DIR, "libs")

sys.path.append(LIB_PATH)

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs


def get_best_transcript(video_id, languages):
    try:
        ytt = YouTubeTranscriptApi()
        transcript_list = ytt.list(video_id)

        try:
            transcript = transcript_list.find_manually_created_transcript(languages)
            return transcript.fetch()
        except NoTranscriptFound:
            pass

        try:
            transcript = transcript_list.find_generated_transcript(languages)
            return transcript.fetch()
        except NoTranscriptFound:
            pass

        raise Exception("There are no transcripts available for this video")

    except TranscriptsDisabled:
        raise Exception("This video has no transcripts")

def extract_video_id(url: str) -> str | None:
    parsed = urlparse(url)

    if parsed.hostname == "youtu.be":
        return parsed.path[1:]

    if parsed.hostname in ["www.youtube.com", "youtube.com", "m.youtube.com"]:
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]

        if parsed.path.startswith("/embed/"):
            return parsed.path.split("/")[2]

        if parsed.path.startswith("/shorts/"):
            return parsed.path.split("/")[2]

    return None

def transcript_txt(link, languages=['ko', 'en']):
    video_id = extract_video_id(link)

    if video_id is None:
        raise Exception("Link is not youtube link")

    transcript = get_best_transcript(video_id, languages)

    full_text = " ".join([segment.text for segment in transcript])

    return full_text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR: Missing URL")
        sys.exit(1)

    url = sys.argv[1]

    try:
        text = transcript_txt(url)

        print("[TRANSCRIPT-START\n"+text+"\n[TRANSCRIPT-END]")

    except Exception as e:
        print('Error:', e)
        sys.exit(1)
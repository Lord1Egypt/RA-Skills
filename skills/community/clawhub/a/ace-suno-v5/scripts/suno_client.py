import requests
import os
import datetime
from typing import Optional, Dict, List, Any


class AceSunoClient:
    """Python client for AceData Suno v5 music generation API"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.acedata.cloud/suno"):
        """
        Initialize the AceData Suno client
        
        Args:
            api_key: AceData API key (defaults to ACE_DATA_API_KEY environment variable)
            base_url: Base URL for the API
        """
        self.api_key = api_key or os.getenv("ACE_DATA_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set as ACE_DATA_API_KEY environment variable")
        
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "accept": "application/json",
            "Content-Type": "application/json",
            "authorization": f"Bearer {self.api_key}"
        })
    
    def generate(
        self,
        prompt: str = "",
        action: str = "generate",
        model: str = "chirp-v5",
        lyric: Optional[str] = None,
        custom: bool = False,
        instrumental: bool = False,
        title: Optional[str] = None,
        style: Optional[str] = None,
        style_negative: Optional[str] = None,
        audio_weight: Optional[float] = None,
        audio_id: Optional[str] = None,
        vocal_gender: Optional[str] = None,
        weirdness: Optional[int] = None,
        lyric_prompt: Optional[str] = None,
        callback_url: Optional[str] = None,
        overpainting_start: Optional[float] = None,
        overpainting_end: Optional[float] = None,
        underpainting_start: Optional[float] = None,
        underpainting_end: Optional[float] = None,
        persona_id: Optional[str] = None,
        continue_at: Optional[float] = None,
        style_influence: Optional[float] = None,
        replace_section_end: Optional[float] = None,
        replace_section_start: Optional[float] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate music with Suno v5 API
        
        Args:
            action: Generation action (generate, extend, cover, etc.)
            prompt: Inspiration mode prompt
            model: Model version (chirp-v3, chirp-v4, chirp-v3-5, chirp-v4-5, chirp-v4-5-plus, chirp-v5)
            lyric: Custom lyrics for custom mode
            custom: Whether to use custom mode (default: False)
            instrumental: Generate instrumental in inspiration mode
            title: Song title for custom mode
            style: Song style for custom mode
            style_negative: Excluded styles
            audio_weight: Reference audio weight (0-1)
            audio_id: Reference audio ID
            vocal_gender: Vocal gender (f for female, m for male)
            weirdness: Weirdness level
            lyric_prompt: Prompt for lyric generation (when custom=true and lyric empty)
            overpainting_start: Add vocals to instrumental - start time (seconds)
            overpainting_end: Add vocals to instrumental - end time (seconds)
            underpainting_start: Add accompaniment to acapella - start time (seconds)
            underpainting_end: Add accompaniment to acapella - end time (seconds)
            persona_id: Artist song ID
            continue_at: Continue existing audio at time (seconds)
            style_influence: Style influence advanced parameter
            replace_section_end: Replace section - end time
            replace_section_start: Replace section - start time
            
        Returns:
            API response with generated audio data
        """
        endpoint = f"{self.base_url}/audios"
        
        # Base required parameters
        payload: Dict[str, Any] = {
            "action": action,
            "model": model
        }
        
        # Only add parameters when they are true or have non-empty values
        if prompt and prompt.strip():
            payload["prompt"] = prompt.strip()
        if custom:
            payload["custom"] = custom  # only send when true
        if instrumental:
            payload["instrumental"] = instrumental  # only send when true
        if lyric and lyric.strip():
            payload["lyric"] = lyric.strip()
        if title and title.strip():
            payload["title"] = title.strip()
        if style and style.strip():
            payload["style"] = style.strip()
        if style_negative and style_negative.strip():
            payload["style_negative"] = style_negative.strip()
        if audio_weight is not None:
            payload["audio_weight"] = audio_weight
        if audio_id and audio_id.strip():
            payload["audio_id"] = audio_id.strip()
        if vocal_gender and vocal_gender.strip():
            payload["vocal_gender"] = vocal_gender.strip()
        if weirdness is not None:
            payload["weirdness"] = weirdness
        if lyric_prompt and lyric_prompt.strip():
            payload["lyric_prompt"] = lyric_prompt.strip()
        if callback_url and callback_url.strip():
            payload["callback_url"] = callback_url.strip()
        if overpainting_start is not None:
            payload["overpainting_start"] = overpainting_start
        if overpainting_end is not None:
            payload["overpainting_end"] = overpainting_end
        if underpainting_start is not None:
            payload["underpainting_start"] = underpainting_start
        if underpainting_end is not None:
            payload["underpainting_end"] = underpainting_end
        if persona_id and persona_id.strip():
            payload["persona_id"] = persona_id.strip()
        if continue_at is not None:
            payload["continue_at"] = continue_at
        if style_influence is not None:
            payload["style_influence"] = style_influence
        if replace_section_end is not None:
            payload["replace_section_end"] = replace_section_end
        if replace_section_start is not None:
            payload["replace_section_start"] = replace_section_start
        
        # Add any additional parameters
        payload.update(kwargs)
        
        response = self.session.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json()
    
    def download_file(self, url: str, output_path: str) -> None:
        """Download file from URL to local path"""
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    
    def save_generation(self, data: List[Dict[str, Any]], base_dir: str = "C:\\Users\\86137\\Desktop\\music") -> str:
        """
        Save generated music and images to desktop music folder with date
        
        Args:
            data: Generated data from API response
            base_dir: Base directory to save files
            
        Returns:
            Path to the created date directory
        """
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        output_dir = os.path.join(base_dir, today)
        os.makedirs(output_dir, exist_ok=True)
        
        for track in data:
            track_id = track["id"]
            title = track.get("title", f"untitled_{track_id}").replace(" ", "_").replace("/", "_")
            
            # Download audio
            if track.get("audio_url"):
                audio_path = os.path.join(output_dir, f"{title}_{track_id}.mp3")
                self.download_file(track["audio_url"], audio_path)
            
            # Download image
            if track.get("image_url"):
                ext = os.path.splitext(track["image_url"])[1] or ".jpg"
                image_path = os.path.join(output_dir, f"{title}_{track_id}{ext}")
                self.download_file(track["image_url"], image_path)
            
            # Save lyric
            if track.get("lyric"):
                lyric_path = os.path.join(output_dir, f"{title}_{track_id}.txt")
                with open(lyric_path, "w", encoding="utf-8") as f:
                    f.write(track["lyric"])
        
        return output_dir

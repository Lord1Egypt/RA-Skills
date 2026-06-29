import os
from pymediainfo import MediaInfo


class MediaUtils:
    @staticmethod
    def get_duration(media_path: str) -> float:
        """Get duration of a media file in milliseconds.
        Args:
            media_path (str): Path to the media file.
            
        Returns:
            int: Duration of the media file in milliseconds.
        """
        if not media_path or os.path.exists(media_path) == False:
            return 0

        try:
            media_info = MediaInfo.parse(media_path)

            if not media_info or not media_info.tracks:
                return 0
            for track in media_info.tracks:
                if hasattr(track, 'duration') and track.duration is not None:
                    return float(track.duration)
            return 0
        except Exception:
            return 0
        
    @staticmethod
    def get_duration_from_url(media_url: str) -> float:
        """Get duration of a media file in milliseconds.
        Args:
            media_url (str): URL to the media file.

        Returns:
            int: Duration of the media file in milliseconds.
        """
        import tempfile
        import requests
        
        temp_path = None
        try:
            resp = requests.get(media_url, stream=True)
            resp.raise_for_status()
            
            temp_fd, temp_path = tempfile.mkstemp(suffix='.mp4')
            os.close(temp_fd)
            
            with open(temp_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            return MediaUtils.get_duration(temp_path)
        except Exception:
            return 0
        finally:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass

    @staticmethod
    def get_resolution(media_path: str) -> int:
        """Get resolution of a media file.
        Args:
            media_path (str): Path to the media file.
            
        Returns:
            int: Resolution of the media file.
        """
        if not media_path or os.path.exists(media_path) == False:
            return 0

        media_info = MediaInfo.parse(media_path)

        if not media_info or not media_info.tracks:
            return 0

        for track in media_info.tracks:
            if hasattr(track, 'sampled_height') and track.sampled_height is not None:
                resolution = int(track.sampled_height)
                return resolution
        return 0
    
    @staticmethod
    def get_resolution_from_url(media_url: str) -> float:
        """Get resolution of a media_url file.
        Args:
            media_url (str): URL to the media file.

        Returns:
            int: Resolution of the media file.
        """
        import tempfile
        import requests
        
        temp_path = None
        try:
            resp = requests.get(media_url, stream=True)
            resp.raise_for_status()
            
            temp_fd, temp_path = tempfile.mkstemp(suffix='.mp4')
            os.close(temp_fd)
            
            with open(temp_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            return MediaUtils.get_resolution(temp_path)
        except Exception:
            return 0
        finally:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
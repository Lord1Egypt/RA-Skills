import requests
from typing import Optional, Dict, Any, List, Union
from requests.models import Response

BASE_URL = "https://emby.example.com/emby"
API_KEY = "652436b1ffa84d9a85f579eeb34b87aa"

HEADERS = {
    "Content-Type": "application/json"
}

def _request(method: str, endpoint: str, params: Optional[Dict] = None, 
             data: Optional[Dict] = None, stream: bool = False) -> Union[Dict, Response]:
    """Base request method"""
    url = f"{BASE_URL}{endpoint}"
    params = params or {}
    params["api_key"] = API_KEY
    
    if method.upper() == "GET":
        resp = requests.get(url, params=params, headers=HEADERS, stream=stream)
    elif method.upper() == "POST":
        resp = requests.post(url, params=params, json=data, headers=HEADERS, stream=stream)
    elif method.upper() == "PUT":
        resp = requests.put(url, params=params, json=data, headers=HEADERS, stream=stream)
    elif method.upper() == "DELETE":
        resp = requests.delete(url, params=params, headers=HEADERS, stream=stream)
    else:
        raise ValueError(f"Unsupported method: {method}")
    
    if stream:
        return resp
    return resp.json()


# ============ Artists ============

def get_artist(artist_type: Optional[str] = None, max_official_rating: Optional[str] = None,
               has_theme_song: Optional[bool] = None, has_theme_video: Optional[bool] = None,
               has_subtitles: Optional[bool] = None, has_special_feature: Optional[bool] = None,
               has_trailer: Optional[bool] = None, is_special_season: Optional[bool] = None,
               adjacent_to: Optional[str] = None, start_item_id: Optional[str] = None,
               min_index_number: Optional[int] = None, min_start_date: Optional[str] = None,
               max_start_date: Optional[str] = None, min_end_date: Optional[str] = None,
               max_end_date: Optional[str] = None, min_players: Optional[int] = None,
               max_players: Optional[int] = None, parent_index_number: Optional[int] = None,
               has_parental_rating: Optional[bool] = None, is_hd: Optional[bool] = None,
               is_unaired: Optional[bool] = None, min_community_rating: Optional[float] = None,
               min_critic_rating: Optional[float] = None, aired_during_season: Optional[int] = None,
               min_premiere_date: Optional[str] = None, min_date_last_saved: Optional[str] = None,
               min_date_last_saved_for_user: Optional[str] = None, max_premiere_date: Optional[str] = None,
               has_overview: Optional[bool] = None, has_imdb_id: Optional[bool] = None,
               has_tmdb_id: Optional[bool] = None, has_tvdb_id: Optional[bool] = None,
               exclude_item_ids: Optional[str] = None, start_index: Optional[int] = None,
               limit: Optional[int] = None, recursive: bool = False, search_term: Optional[str] = None,
               sort_order: Optional[str] = None, parent_id: Optional[str] = None,
               fields: Optional[str] = None, exclude_item_types: Optional[str] = None,
               include_item_types: Optional[str] = None, any_provider_id_equals: Optional[str] = None,
               filters: Optional[str] = None, is_favorite: Optional[bool] = None,
               is_movie: Optional[bool] = None, is_series: Optional[bool] = None,
               is_folder: Optional[bool] = None, is_news: Optional[bool] = None,
               is_kids: Optional[bool] = None, is_sports: Optional[bool] = None,
               is_new: Optional[bool] = None, is_premiere: Optional[bool] = None,
               is_new_or_premiere: Optional[bool] = None, is_repeat: Optional[bool] = None,
               project_to_media: bool = False, media_types: Optional[str] = None,
               image_types: Optional[str] = None, sort_by: Optional[str] = None,
               is_played: Optional[bool] = None, genres: Optional[str] = None,
               official_ratings: Optional[str] = None, tags: Optional[str] = None,
               exclude_tags: Optional[str] = None, years: Optional[str] = None,
               enable_images: Optional[bool] = None, enable_user_data: Optional[bool] = None,
               image_type_limit: Optional[int] = None, enable_image_types: Optional[str] = None,
               person: Optional[str] = None, person_ids: Optional[str] = None,
               person_types: Optional[str] = None, studios: Optional[str] = None,
               studio_ids: Optional[str] = None, artists: Optional[str] = None,
               artist_ids: Optional[str] = None, albums: Optional[str] = None,
               ids: Optional[str] = None, video_types: Optional[str] = None,
               containers: Optional[str] = None, audio_codecs: Optional[str] = None,
               audio_layouts: Optional[str] = None, video_codecs: Optional[str] = None,
               extended_video_types: Optional[str] = None, subtitle_codecs: Optional[str] = None,
               path: Optional[str] = None, user_id: Optional[str] = None,
               min_official_rating: Optional[str] = None, is_locked: Optional[bool] = None,
               is_place_holder: Optional[bool] = None, has_official_rating: Optional[bool] = None,
               group_items_into_collections: bool = False, is_3d: Optional[bool] = None,
               series_status: Optional[str] = None, name_starts_with_or_greater: Optional[str] = None,
               artist_starts_with_or_greater: Optional[str] = None,
               album_artist_starts_with_or_greater: Optional[str] = None,
               name_starts_with: Optional[str] = None, name_less_than: Optional[str] = None) -> Dict:
    """Gets all artists from a given item, folder, or the entire library"""
    params = {k: v for k, v in locals().items() if v is not None and k not in ('artist_type', 'max_official_rating', 'search_term', 'sort_order', 'parent_id', 'fields', 'exclude_item_types', 'include_item_types', 'any_provider_id_equals', 'filters', 'media_types', 'image_types', 'sort_by', 'genres', 'official_ratings', 'tags', 'exclude_tags', 'years', 'enable_image_types', 'person', 'person_ids', 'person_types', 'studios', 'studio_ids', 'artists', 'artist_ids', 'albums', 'ids', 'video_types', 'containers', 'audio_codecs', 'audio_layouts', 'video_codecs', 'extended_video_types', 'subtitle_codecs', 'path', 'user_id', 'series_status', 'name_starts_with_or_greater', 'artist_starts_with_or_greater', 'album_artist_starts_with_or_greater', 'name_starts_with', 'name_less_than')}
    if artist_type: params["ArtistType"] = artist_type
    if max_official_rating: params["MaxOfficialRating"] = max_official_rating
    if search_term: params["SearchTerm"] = search_term
    if sort_order: params["SortOrder"] = sort_order
    if parent_id: params["ParentId"] = parent_id
    if fields: params["Fields"] = fields
    if exclude_item_types: params["ExcludeItemTypes"] = exclude_item_types
    if include_item_types: params["IncludeItemTypes"] = include_item_types
    if any_provider_id_equals: params["AnyProviderIdEquals"] = any_provider_id_equals
    if filters: params["Filters"] = filters
    if media_types: params["MediaTypes"] = media_types
    if image_types: params["ImageTypes"] = image_types
    if sort_by: params["SortBy"] = sort_by
    if genres: params["Genres"] = genres
    if official_ratings: params["OfficialRatings"] = official_ratings
    if tags: params["Tags"] = tags
    if exclude_tags: params["ExcludeTags"] = exclude_tags
    if years: params["Years"] = years
    if enable_image_types: params["EnableImageTypes"] = enable_image_types
    if person: params["Person"] = person
    if person_ids: params["PersonIds"] = person_ids
    if person_types: params["PersonTypes"] = person_types
    if studios: params["Studios"] = studios
    if studio_ids: params["StudioIds"] = studio_ids
    if artists: params["Artists"] = artists
    if artist_ids: params["ArtistIds"] = artist_ids
    if albums: params["Albums"] = albums
    if ids: params["Ids"] = ids
    if video_types: params["VideoTypes"] = video_types
    if containers: params["Containers"] = containers
    if audio_codecs: params["AudioCodecs"] = audio_codecs
    if audio_layouts: params["AudioLayouts"] = audio_layouts
    if video_codecs: params["VideoCodecs"] = video_codecs
    if extended_video_types: params["ExtendedVideoTypes"] = extended_video_types
    if subtitle_codecs: params["SubtitleCodecs"] = subtitle_codecs
    if path: params["Path"] = path
    if user_id: params["UserId"] = user_id
    if series_status: params["SeriesStatus"] = series_status
    if name_starts_with_or_greater: params["NameStartsWithOrGreater"] = name_starts_with_or_greater
    if artist_starts_with_or_greater: params["ArtistStartsWithOrGreater"] = artist_starts_with_or_greater
    if album_artist_starts_with_or_greater: params["AlbumArtistStartsWithOrGreater"] = album_artist_starts_with_or_greater
    if name_starts_with: params["NameStartsWith"] = name_starts_with
    if name_less_than: params["NameLessThan"] = name_less_than
    params["Recursive"] = recursive
    params["ProjectToMedia"] = project_to_media
    if group_items_into_collections: params["GroupItemsIntoCollections"] = group_items_into_collections
    return _request("GET", "/Artists", params)


def get_artist_by_name(name: str) -> Dict:
    """Gets an artist by name"""
    return _request("GET", f"/Artists/{name}")


def get_album_artists(**kwargs) -> Dict:
    """Gets all album artists"""
    params = {k: v for k, v in kwargs.items() if v is not None}
    return _request("GET", "/Artists/AlbumArtists", params)


def get_artists_prefixes(start_index: Optional[int] = None, limit: Optional[int] = None) -> Dict:
    """Gets artists by prefix"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    return _request("GET", "/Artists/Prefixes", params)


def get_artists_instant_mix(artist_type: Optional[str] = None, **kwargs) -> Dict:
    """Creates an instant playlist based on a given artist"""
    params = {"api_key": API_KEY}
    if artist_type: params["ArtistType"] = artist_type
    params.update({k: v for k, v in kwargs.items() if v is not None})
    return _request("GET", "/Artists/InstantMix", params)


# ============ Albums ============

def get_albums_instant_mix(id: str, **kwargs) -> Dict:
    """Creates an instant playlist based on a given album"""
    params = {k: v for k, v in kwargs.items() if v is not None}
    return _request("GET", f"/Albums/{id}/InstantMix", params)


# ============ Audio/Video Codecs ============

def get_audio_codecs(**kwargs) -> Dict:
    """Gets audio codecs"""
    params = {k: v for k, v in kwargs.items() if v is not None}
    return _request("GET", "/AudioCodecs", params)


def get_audio_layouts(**kwargs) -> Dict:
    """Gets audio layouts"""
    params = {k: v for k, v in kwargs.items() if v is not None}
    return _request("GET", "/AudioLayouts", params)


def get_video_codecs(**kwargs) -> Dict:
    """Gets video codecs"""
    params = {k: v for k, v in kwargs.items() if v is not None}
    return _request("GET", "/VideoCodecs", params)


def get_subtitle_codecs(**kwargs) -> Dict:
    """Gets subtitle codecs"""
    params = {k: v for k, v in kwargs.items() if v is not None}
    return _request("GET", "/SubtitleCodecs", params)


def get_containers(**kwargs) -> Dict:
    """Gets container types"""
    params = {k: v for k, v in kwargs.items() if v is not None}
    return _request("GET", "/Containers", params)


def get_extended_video_types(**kwargs) -> Dict:
    """Gets extended video types"""
    params = {k: v for k, v in kwargs.items() if v is not None}
    return _request("GET", "/ExtendedVideoTypes", params)


def get_stream_languages(**kwargs) -> Dict:
    """Gets stream languages"""
    params = {k: v for k, v in kwargs.items() if v is not None}
    return _request("GET", "/StreamLanguages", params)


# ============ Channels & Collections ============

def get_channels(start_index: Optional[int] = None, limit: Optional[int] = None) -> Dict:
    """Gets available channels"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    return _request("GET", "/Channels", params)


def post_collections(name: str, parent_id: Optional[str] = None, 
                    is_locked: Optional[bool] = None) -> Dict:
    """Creates a new collection"""
    data = {"Name": name}
    if parent_id: data["ParentId"] = parent_id
    if is_locked is not None: data["IsLocked"] = is_locked
    return _request("POST", "/Collections", data=data)


# ============ Devices ============

def get_devices(start_index: Optional[int] = None, limit: Optional[int] = None) -> Dict:
    """Gets all devices"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    return _request("GET", "/Devices", params)


def delete_devices(device_id: str) -> Dict:
    """Deletes a device"""
    return _request("DELETE", f"/Devices?DeviceId={device_id}")


def get_devices_options(device_id: Optional[str] = None) -> Dict:
    """Gets options for a device"""
    params = {}
    if device_id: params["DeviceId"] = device_id
    return _request("GET", "/Devices/Options", params)


def post_devices_options(device_id: str, options: Dict) -> Dict:
    """Updates device options"""
    params = {"DeviceId": device_id}
    return _request("POST", "/Devices/Options", params=params, data=options)


def get_devices_info(device_id: Optional[str] = None) -> Dict:
    """Gets info for a device"""
    params = {}
    if device_id: params["DeviceId"] = device_id
    return _request("GET", "/Devices/Info", params)


def get_devices_camera_uploads(user_id: Optional[str] = None) -> Dict:
    """Gets camera upload history"""
    params = {}
    if user_id: params["UserId"] = user_id
    return _request("GET", "/Devices/CameraUploads", params)


def post_devices_camera_uploads(device_id: str, file_path: str) -> Response:
    """Uploads camera content (stream)"""
    params = {"DeviceId": device_id}
    with open(file_path, 'rb') as f:
        files = {'file': f}
        url = f"{BASE_URL}/Devices/CameraUploads"
        params["api_key"] = API_KEY
        return requests.post(url, params=params, files=files)


def post_devices_delete(device_ids: List[str]) -> Dict:
    """Deletes devices"""
    data = {"DeviceIds": device_ids}
    return _request("POST", "/Devices/Delete", data=data)


# ============ Genres ============

def get_genres(start_index: Optional[int] = None, limit: Optional[int] = None,
               search_term: Optional[str] = None) -> Dict:
    """Gets all genres"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    if search_term: params["SearchTerm"] = search_term
    return _request("GET", "/Genres", params)


def get_genre_by_name(name: str) -> Dict:
    """Gets genre by name"""
    return _request("GET", f"/Genres/{name}")


def get_music_genres(**kwargs) -> Dict:
    """Gets all music genres"""
    params = {k: v for k, v in kwargs.items() if v is not None}
    return _request("GET", "/MusicGenres", params)


def get_music_genre_by_name(name: str) -> Dict:
    """Gets music genre by name"""
    return _request("GET", f"/MusicGenres/{name}")


def get_music_genres_instant_mix(**kwargs) -> Dict:
    """Creates an instant playlist based on a music genre"""
    params = {k: v for k, v in kwargs.items() if v is not None}
    return _request("GET", "/MusicGenres/InstantMix", params)


def get_game_genres(**kwargs) -> Dict:
    """Gets all game genres"""
    params = {k: v for k, v in kwargs.items() if v is not None}
    return _request("GET", "/GameGenres", params)


def get_game_genre_by_name(name: str) -> Dict:
    """Gets game genre by name"""
    return _request("GET", f"/GameGenres/{name}")


def get_official_ratings(**kwargs) -> Dict:
    """Gets official ratings"""
    params = {k: v for k, v in kwargs.items() if v is not None}
    return _request("GET", "/OfficialRatings", params)


# ============ Items ============

def get_items(start_index: Optional[int] = None, limit: Optional[int] = None,
              recursive: bool = False, search_term: Optional[str] = None,
              sort_by: Optional[str] = None, sort_order: Optional[str] = None,
              parent_id: Optional[str] = None, fields: Optional[str] = None,
              include_item_types: Optional[str] = None, exclude_item_types: Optional[str] = None,
              filters: Optional[str] = None, **kwargs) -> Dict:
    """Gets items based on query"""
    params = {"Recursive": recursive}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    if search_term: params["SearchTerm"] = search_term
    if sort_by: params["SortBy"] = sort_by
    if sort_order: params["SortOrder"] = sort_order
    if parent_id: params["ParentId"] = parent_id
    if fields: params["Fields"] = fields
    if include_item_types: params["IncludeItemTypes"] = include_item_types
    if exclude_item_types: params["ExcludeItemTypes"] = exclude_item_types
    if filters: params["Filters"] = filters
    params.update({k: v for k, v in kwargs.items() if v is not None})
    return _request("GET", "/Items", params)


def delete_items(item_ids: List[str]) -> Dict:
    """Deletes items from library"""
    params = {"ItemIds": ",".join(item_ids)}
    return _request("DELETE", "/Items", params)


def get_item_by_id(id: str, fields: Optional[str] = None) -> Dict:
    """Gets item by ID"""
    params = {}
    if fields: params["Fields"] = fields
    return _request("GET", f"/Items/{id}", params)


def delete_item_by_id(id: str) -> Dict:
    """Deletes item by ID"""
    return _request("DELETE", f"/Items/{id}")


def update_item(id: str, data: Dict) -> Dict:
    """Updates an item"""
    return _request("POST", f"/Items/{id}", data=data)


def get_items_prefixes(start_index: Optional[int] = None, limit: Optional[int] = None) -> Dict:
    """Gets items by prefix"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    return _request("GET", "/Items/Prefixes", params)


def post_items_access(item_ids: List[str], user_ids: List[str]) -> Dict:
    """Posts item access"""
    data = {"ItemIds": item_ids, "UserIds": user_ids}
    return _request("POST", "/Items/Access", data=data)


def get_items_counts(user_id: Optional[str] = None, 
                    include_disabled: bool = False) -> Dict:
    """Gets item counts"""
    params = {"IncludeDisabledUsers": include_disabled}
    if user_id: params["UserId"] = user_id
    return _request("GET", "/Items/Counts", params)


def get_items_intros(item_id: str) -> Dict:
    """Gets item intros"""
    return _request("GET", f"/Items/{item_id}/Intros")


def post_items_delete(item_ids: List[str]) -> Dict:
    """Deletes items (batch)"""
    data = {"ItemIds": item_ids}
    return _request("POST", "/Items/Delete", data=data)


def get_item_types() -> Dict:
    """Gets item types"""
    return _request("GET", "/ItemTypes")


# ============ Item Images (Stream) ============

def get_item_image(item_id: str, image_type: str, index: int = 0,
                   tag: Optional[str] = None, format: str = "original",
                   max_width: Optional[int] = None, max_height: Optional[int] = None,
                   percent_played: Optional[float] = None, 
                   unplayed_count: Optional[int] = None) -> Response:
    """Gets item image (stream)"""
    params = {"api_key": API_KEY}
    if tag: params["Tag"] = tag
    if format: params["Format"] = format
    if max_width: params["MaxWidth"] = max_width
    if max_height: params["MaxHeight"] = max_height
    if percent_played: params["PercentPlayed"] = percent_played
    if unplayed_count is not None: params["UnPlayedCount"] = unplayed_count
    
    url = f"{BASE_URL}/Items/{item_id}/Images/{image_type}/{index}"
    return requests.get(url, params=params, stream=True)


def head_item_image(item_id: str, image_type: str, index: int = 0,
                    tag: Optional[str] = None, format: str = "original",
                    max_width: Optional[int] = None, max_height: Optional[int] = None,
                    percent_played: Optional[float] = None,
                    unplayed_count: Optional[int] = None) -> Response:
    """Gets item image headers"""
    params = {"api_key": API_KEY}
    if tag: params["Tag"] = tag
    if format: params["Format"] = format
    if max_width: params["MaxWidth"] = max_width
    if max_height: params["MaxHeight"] = max_height
    if percent_played: params["PercentPlayed"] = percent_played
    if unplayed_count is not None: params["UnPlayedCount"] = unplayed_count
    
    url = f"{BASE_URL}/Items/{item_id}/Images/{image_type}/{index}"
    return requests.head(url, params=params)


def download_item_image(item_id: str, image_type: str, index: int = 0,
                        output_path: str = None) -> bytes:
    """Downloads item image to file or returns bytes"""
    resp = get_item_image(item_id, image_type, index)
    if output_path:
        with open(output_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return None
    return resp.content


# ============ Users ============

def get_public_users() -> Dict:
    """Gets publicly visible users"""
    return _request("GET", "/Users/Public")


def query_users(start_index: Optional[int] = None, limit: Optional[int] = None) -> Dict:
    """Gets list of users"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    return _request("GET", "/Users/Query", params)


def get_users_prefixes(start_index: Optional[int] = None, limit: Optional[int] = None) -> Dict:
    """Gets users by prefix"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    return _request("GET", "/Users/Prefixes", params)


def get_users_item_access() -> Dict:
    """Gets users with item access"""
    return _request("GET", "/Users/ItemAccess")


def get_user_by_id(id: str) -> Dict:
    """Gets user by ID"""
    return _request("GET", f"/Users/{id}")


def delete_user(id: str) -> Dict:
    """Deletes user"""
    return _request("DELETE", f"/Users/{id}")


def update_user(id: str, data: Dict) -> Dict:
    """Updates user"""
    return _request("POST", f"/Users/{id}", data=data)


def authenticate_user(username: str, password: str, 
                     pw: Optional[str] = None) -> Dict:
    """Authenticates user by name"""
    data = {"Username": username, "Password": password}
    if pw: data["Pw"] = pw
    return _request("POST", "/Users/AuthenticateByName", data=data)


def create_user(username: str, password: Optional[str] = None,
               auth_provider: Optional[str] = None) -> Dict:
    """Creates new user"""
    data = {"Username": username}
    if password: data["Password"] = password
    if auth_provider: data["AuthProvider"] = auth_provider
    return _request("POST", "/Users/New", data=data)


def forgot_password(username: str) -> Dict:
    """Initiates forgot password"""
    data = {"Username": username}
    return _request("POST", "/Users/ForgotPassword", data=data)


def get_user_settings(user_id: str) -> Dict:
    """Gets user settings"""
    return _request("GET", f"/UserSettings/{user_id}")


def update_user_settings(user_id: str, data: Dict) -> Dict:
    """Updates user settings"""
    return _request("POST", f"/UserSettings/{user_id}", data=data)


# ============ User Data ============

def get_played_items(user_id: str, start_index: Optional[int] = None,
                    limit: Optional[int] = None) -> Dict:
    """Gets played items"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    return _request("GET", f"/Users/{user_id}/PlayedItems", params)


def mark_item_played(user_id: str, item_id: str, 
                    date_played: Optional[str] = None) -> Dict:
    """Marks item as played"""
    params = {}
    if date_played: params["DatePlayed"] = date_played
    return _request("POST", f"/Users/{user_id}/PlayedItems/{item_id}", params)


def mark_item_unplayed(user_id: str, item_id: str) -> Dict:
    """Marks item as unplayed"""
    return _request("DELETE", f"/Users/{user_id}/PlayedItems/{item_id}")


def get_favorite_items(user_id: str, start_index: Optional[int] = None,
                      limit: Optional[int] = None) -> Dict:
    """Gets favorite items"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    return _request("GET", f"/Users/{user_id}/FavoriteItems", params)


def mark_item_favorite(user_id: str, item_id: str) -> Dict:
    """Marks item as favorite"""
    return _request("POST", f"/Users/{user_id}/FavoriteItems/{item_id}")


def remove_favorite(user_id: str, item_id: str) -> Dict:
    """Removes item from favorites"""
    return _request("DELETE", f"/Users/{user_id}/FavoriteItems/{item_id}")


def get_resume_items(user_id: str, start_index: Optional[int] = None,
                    limit: Optional[int] = None) -> Dict:
    """Gets resume items"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    return _request("GET", f"/Users/{user_id}/ResumeItems", params)


# ============ Sessions ============

def get_sessions() -> Dict:
    """Gets list of sessions"""
    return _request("GET", "/Sessions")


# ============ Playlists ============

def create_playlist(name: str, item_ids: Optional[List[str]] = None,
                   parent_id: Optional[str] = None,
                   media_type: Optional[str] = None) -> Dict:
    """Creates new playlist"""
    data = {"Name": name}
    if item_ids: data["ItemIds"] = item_ids
    if parent_id: data["ParentId"] = parent_id
    if media_type: data["MediaType"] = media_type
    return _request("POST", "/Playlists", data=data)


# ============ Plugins ============

def get_plugins() -> Dict:
    """Gets installed plugins"""
    return _request("GET", "/Plugins")


# ============ Scheduled Tasks ============

def get_scheduled_tasks() -> Dict:
    """Gets scheduled tasks"""
    return _request("GET", "/ScheduledTasks")


# ============ Library ============

def get_libraries_available_options() -> Dict:
    """Gets available library options"""
    return _request("GET", "/Libraries/AvailableOptions")


def get_library_selectable_media_folders() -> Dict:
    """Gets selectable media folders"""
    return _request("GET", "/Library/SelectableMediaFolders")


def get_library_media_folders(start_index: Optional[int] = None,
                              limit: Optional[int] = None) -> Dict:
    """Gets media folders"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    return _request("GET", "/Library/MediaFolders", params)


def get_library_physical_paths() -> Dict:
    """Gets physical paths"""
    return _request("GET", "/Library/PhysicalPaths")


def refresh_library(item_id: Optional[str] = None,
                   notification_mode: Optional[str] = None) -> Dict:
    """Refreshes library"""
    params = {}
    if item_id: params["ItemId"] = item_id
    if notification_mode: params["NotificationMode"] = notification_mode
    return _request("POST", "/Library/Refresh", params)


def create_virtual_folder(name: str, library_type: str,
                         paths: Optional[List[str]] = None) -> Dict:
    """Creates virtual folder"""
    data = {"Name": name, "LibraryType": library_type}
    if paths: data["Paths"] = paths
    return _request("POST", "/Library/VirtualFolders", data=data)


def delete_virtual_folder(name: str) -> Dict:
    """Deletes virtual folder"""
    params = {"Name": name}
    return _request("DELETE", "/Library/VirtualFolders", params)


# ============ Live TV ============

def get_live_tv_channel_tags(start_index: Optional[int] = None,
                             limit: Optional[int] = None) -> Dict:
    """Gets channel tags"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    return _request("GET", "/LiveTv/ChannelTags", params)


def get_live_tv_folder() -> Dict:
    """Gets live TV folder"""
    return _request("GET", "/LiveTv/Folder")


def get_live_tv_channel_mappings(tuner_host_id: Optional[str] = None,
                                 provider_id: Optional[str] = None) -> Dict:
    """Gets channel mappings"""
    params = {}
    if tuner_host_id: params["TunerHostId"] = tuner_host_id
    if provider_id: params["ProviderId"] = provider_id
    return _request("GET", "/LiveTv/ChannelMappings", params)


def get_live_tv_channel_mapping_options(tuner_host_type: Optional[str] = None) -> Dict:
    """Gets channel mapping options"""
    params = {}
    if tuner_host_type: params["TunerHostType"] = tuner_host_type
    return _request("GET", "/LiveTv/ChannelMappingOptions", params)


def get_live_tv_listing_providers() -> Dict:
    """Gets listing providers"""
    return _request("GET", "/LiveTv/ListingProviders")


def get_live_tv_tuner_hosts() -> Dict:
    """Gets tuner hosts"""
    return _request("GET", "/LiveTv/TunerHosts")


def get_live_tv_info() -> Dict:
    """Gets live TV info"""
    return _request("GET", "/LiveTv/Info")


def get_live_tv_epg(channel_id: Optional[str] = None,
                   start_time: Optional[str] = None,
                   end_time: Optional[str] = None) -> Dict:
    """Gets EPG guide"""
    params = {}
    if channel_id: params["ChannelId"] = channel_id
    if start_time: params["StartTime"] = start_time
    if end_time: params["EndTime"] = end_time
    return _request("GET", "/LiveTv/EPG", params)


def get_live_tv_channels(start_index: Optional[int] = None,
                        limit: Optional[int] = None,
                        user_id: Optional[str] = None) -> Dict:
    """Gets channels"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    if user_id: params["UserId"] = user_id
    return _request("GET", "/LiveTv/Channels", params)


def get_live_tv_programs(channel_id: Optional[str] = None,
                        start_time: Optional[str] = None,
                        end_time: Optional[str] = None,
                        is_running: Optional[bool] = None,
                        **kwargs) -> Dict:
    """Gets programs"""
    params = {}
    if channel_id: params["ChannelId"] = channel_id
    if start_time: params["StartTime"] = start_time
    if end_time: params["EndTime"] = end_time
    if is_running is not None: params["IsRunning"] = is_running
    params.update({k: v for k, v in kwargs.items() if v is not None})
    return _request("GET", "/LiveTv/Programs", params)


def get_live_tv_recordings(start_index: Optional[int] = None,
                          limit: Optional[int] = None,
                          status: Optional[str] = None,
                          **kwargs) -> Dict:
    """Gets recordings"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    if status: params["Status"] = status
    params.update({k: v for k, v in kwargs.items() if v is not None})
    return _request("GET", "/LiveTv/Recordings", params)


def get_live_tv_timers(is_active: Optional[bool] = None,
                      is_series: Optional[bool] = None) -> Dict:
    """Gets timers"""
    params = {}
    if is_active is not None: params["IsActive"] = is_active
    if is_series is not None: params["IsSeries"] = is_series
    return _request("GET", "/LiveTv/Timers", params)


def create_live_tv_timer(data: Dict) -> Dict:
    """Creates live TV timer"""
    return _request("POST", "/LiveTv/Timers", data=data)


def get_live_tv_series_timers(start_index: Optional[int] = None,
                             limit: Optional[int] = None) -> Dict:
    """Gets series timers"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    return _request("GET", "/LiveTv/SeriesTimers", params)


def create_live_tv_series_timer(data: Dict) -> Dict:
    """Creates live TV series timer"""
    return _request("POST", "/LiveTv/SeriesTimers", data=data)


def get_live_tv_guide_info() -> Dict:
    """Gets guide info"""
    return _request("GET", "/LiveTv/GuideInfo")


def get_live_tv_available_recording_options() -> Dict:
    """Gets available recording options"""
    return _request("GET", "/LiveTv/AvailableRecordingOptions")


# ============ Live Streams ============

def open_live_stream(stream_id: Optional[str] = None,
                    media_source_id: Optional[str] = None,
                    live_stream_id: Optional[str] = None,
                    play_session_id: Optional[str] = None,
                    max_streaming_bitrate: Optional[int] = None,
                    start_time_ticks: Optional[int] = None,
                    video_codec: Optional[str] = None,
                    audio_codec: Optional[str] = None,
                    transcoding_container: Optional[str] = None,
                    transcoding_protocol: Optional[str] = None,
                    latency_mode: Optional[str] = None,
                    device_profile: Optional[Dict] = None) -> Dict:
    """Opens live stream"""
    data = {}
    if stream_id: data["StreamId"] = stream_id
    if media_source_id: data["MediaSourceId"] = media_source_id
    if live_stream_id: data["LiveStreamId"] = live_stream_id
    if play_session_id: data["PlaySessionId"] = play_session_id
    if max_streaming_bitrate: data["MaxStreamingBitrate"] = max_streaming_bitrate
    if start_time_ticks: data["StartTimeTicks"] = start_time_ticks
    if video_codec: data["VideoCodec"] = video_codec
    if audio_codec: data["AudioCodec"] = audio_codec
    if transcoding_container: data["TranscodingContainer"] = transcoding_container
    if transcoding_protocol: data["TranscodingProtocol"] = transcoding_protocol
    if latency_mode: data["LatencyMode"] = latency_mode
    if device_profile: data["DeviceProfile"] = device_profile
    return _request("POST", "/LiveStreams/Open", data=data)


def close_live_stream(live_stream_id: str) -> Dict:
    """Closes live stream"""
    data = {"LiveStreamId": live_stream_id}
    return _request("POST", "/LiveStreams/Close", data=data)


def post_live_stream_media_info(live_stream_id: str,
                                media_info: Dict) -> Dict:
    """Posts media info"""
    data = {"LiveStreamId": live_stream_id, "MediaInfo": media_info}
    return _request("POST", "/LiveStreams/MediaInfo", data=data)


# ============ Localization ============

def get_localization_parental_ratings() -> Dict:
    """Gets parental ratings"""
    return _request("GET", "/Localization/ParentalRatings")


def get_localization_options() -> Dict:
    """Gets localization options"""
    return _request("GET", "/Localization/Options")


def get_localization_countries() -> Dict:
    """Gets countries"""
    return _request("GET", "/Localization/Countries")


def get_localization_cultures() -> Dict:
    """Gets cultures"""
    return _request("GET", "/Localization/Cultures")


# ============ Movies ============

def get_movies_recommendations(category_id: Optional[str] = None,
                               start_index: Optional[int] = None,
                               limit: Optional[int] = None) -> Dict:
    """Gets movie recommendations"""
    params = {}
    if category_id: params["CategoryId"] = category_id
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    return _request("GET", "/Movies/Recommendations", params)


# ============ Audio Books ============

def get_audiobooks_next_up(user_id: Optional[str] = None,
                          start_index: Optional[int] = None,
                          limit: Optional[int] = None) -> Dict:
    """Gets next up audiobooks"""
    params = {}
    if user_id: params["UserId"] = user_id
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    return _request("GET", "/AudioBooks/NextUp", params)


# ============ Authentication ============

def get_auth_providers() -> Dict:
    """Gets auth providers"""
    return _request("GET", "/Auth/Providers")


def create_auth_key(app_name: str, app_version: Optional[str] = None,
                   device_id: Optional[str] = None,
                   device_name: Optional[str] = None) -> Dict:
    """Creates auth key"""
    data = {"App": app_name}
    if app_version: data["AppVersion"] = app_version
    if device_id: data["DeviceId"] = device_id
    if device_name: data["DeviceName"] = device_name
    return _request("POST", "/Auth/Keys", data=data)


def get_auth_keys() -> Dict:
    """Gets auth keys"""
    return _request("GET", "/Auth/Keys")


# ============ Backup ============

def restore_backup(data: bytes, file_name: str) -> Response:
    """Restores backup (stream)"""
    url = f"{BASE_URL}/BackupRestore/Restore"
    files = {'file': (file_name, data)}
    return requests.post(url, files=files)


def restore_backup_data(data: Dict) -> Dict:
    """Restores backup data"""
    return _request("POST", "/BackupRestore/RestoreData", data=data)


def get_backup_info() -> Dict:
    """Gets backup info"""
    return _request("GET", "/BackupRestore/BackupInfo")


# ============ Branding ============

def get_branding_configuration() -> Dict:
    """Gets branding configuration"""
    return _request("GET", "/Branding/Configuration")


def get_branding_css() -> Dict:
    """Gets custom CSS"""
    return _request("GET", "/Branding/Css")


def get_branding_css_content() -> str:
    """Gets custom CSS content"""
    url = f"{BASE_URL}/Branding/Css/Css"
    params = {"api_key": API_KEY}
    resp = requests.get(url, params=params)
    return resp.text


# ============ Connect ============

def get_connect_pending() -> Dict:
    """Gets pending connect requests"""
    return _request("GET", "/Connect/Pending")


def get_connect_exchange(connect_user_id: str) -> Dict:
    """Gets exchange info"""
    return _request("GET", f"/Connect/Exchange?ConnectUserId={connect_user_id}")


# ============ Display Preferences ============

def get_display_preferences(id: str, user_id: Optional[str] = None) -> Dict:
    """Gets display preferences"""
    params = {}
    if user_id: params["UserId"] = user_id
    return _request("GET", f"/DisplayPreferences/{id}", params)


def update_display_preferences(display_preferences_id: str, data: Dict) -> Dict:
    """Updates display preferences"""
    return _request("POST", f"/DisplayPreferences/{display_preferences_id}", data=data)


# ============ DLNA ============

def get_dlna_profile_infos() -> Dict:
    """Gets DLNA profiles"""
    return _request("GET", "/Dlna/ProfileInfos")


def create_dlna_profile(data: Dict) -> Dict:
    """Creates DLNA profile"""
    return _request("POST", "/Dlna/Profiles", data=data)


# ============ Encoding ============

def get_encoding_tone_map_options() -> Dict:
    """Gets tone map options"""
    return _request("GET", "/Encoding/ToneMapOptions")


def get_encoding_full_tone_map_options() -> Dict:
    """Gets full tone map options"""
    return _request("GET", "/Encoding/FullToneMapOptions")


def post_encoding_full_tone_map_options(data: Dict) -> Dict:
    """Posts full tone map options"""
    return _request("POST", "/Encoding/FullToneMapOptions", data=data)


def get_encoding_public_tone_map_options() -> Dict:
    """Gets public tone map options"""
    return _request("GET", "/Encoding/PublicToneMapOptions")


def post_encoding_public_tone_map_options(data: Dict) -> Dict:
    """Posts public tone map options"""
    return _request("POST", "/Encoding/PublicToneMapOptions", data=data)


def get_encoding_subtitle_options() -> Dict:
    """Gets subtitle options"""
    return _request("GET", "/Encoding/SubtitleOptions")


def post_encoding_subtitle_options(data: Dict) -> Dict:
    """Posts subtitle options"""
    return _request("POST", "/Encoding/SubtitleOptions", data=data)


def get_encoding_ffmpeg_options() -> Dict:
    """Gets FFmpeg options"""
    return _request("GET", "/Encoding/FfmpegOptions")


def post_encoding_ffmpeg_options(data: Dict) -> Dict:
    """Posts FFmpeg options"""
    return _request("POST", "/Encoding/FfmpegOptions", data=data)


def get_encoding_codec_parameters() -> Dict:
    """Gets codec parameters"""
    return _request("GET", "/Encoding/CodecParameters")


def post_encoding_codec_parameters(data: Dict) -> Dict:
    """Posts codec parameters"""
    return _request("POST", "/Encoding/CodecParameters", data=data)


# ============ Environment ============

def validate_path(path: str) -> Dict:
    """Validates path"""
    data = {"Path": path}
    return _request("POST", "/Environment/ValidatePath", data=data)


def get_environment_default_directory_browser() -> Dict:
    """Gets default directory browser"""
    return _request("GET", "/Environment/DefaultDirectoryBrowser")


def get_environment_directory_contents(path: str) -> Dict:
    """Gets directory contents"""
    params = {"Path": path}
    return _request("GET", "/Environment/DirectoryContents", params)


def post_environment_directory_contents(path: str, data: Dict) -> Dict:
    """Posts directory contents"""
    return _request("POST", f"/Environment/DirectoryContents?Path={path}", data=data)


def get_environment_network_shares(path: Optional[str] = None) -> Dict:
    """Gets network shares"""
    params = {}
    if path: params["Path"] = path
    return _request("GET", "/Environment/NetworkShares", params)


def get_environment_drives() -> Dict:
    """Gets drives"""
    return _request("GET", "/Environment/Drives")


def get_environment_network_devices() -> Dict:
    """Gets network devices"""
    return _request("GET", "/Environment/NetworkDevices")


def get_environment_parent_path(path: str) -> Dict:
    """Gets parent path"""
    params = {"Path": path}
    return _request("GET", "/Environment/ParentPath", params)


# ============ Images ============

def get_remote_images(search_term: Optional[str] = None,
                     type: Optional[str] = None,
                     limit: Optional[int] = None) -> Dict:
    """Gets remote images"""
    params = {}
    if search_term: params["SearchTerm"] = search_term
    if type: params["Type"] = type
    if limit: params["Limit"] = limit
    return _request("GET", "/Images/Remote", params)


# ============ Packages ============

def get_packages(start_index: Optional[int] = None,
                limit: Optional[int] = None) -> Dict:
    """Gets available packages"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    return _request("GET", "/Packages", params)


# ============ Persons ============

def get_persons(start_index: Optional[int] = None,
               limit: Optional[int] = None,
               search_term: Optional[str] = None) -> Dict:
    """Gets all persons"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    if search_term: params["SearchTerm"] = search_term
    return _request("GET", "/Persons", params)


# ============ Studios ============

def get_studios(start_index: Optional[int] = None,
               limit: Optional[int] = None,
               search_term: Optional[str] = None) -> Dict:
    """Gets all studios"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    if search_term: params["SearchTerm"] = search_term
    return _request("GET", "/Studios", params)


# ============ Tags ============

def get_tags(start_index: Optional[int] = None,
            limit: Optional[int] = None) -> Dict:
    """Gets all tags"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    return _request("GET", "/Tags", params)


# ============ Trailers ============

def get_trailers(start_index: Optional[int] = None,
                limit: Optional[int] = None,
                search_term: Optional[str] = None) -> Dict:
    """Finds similar trailers"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    if search_term: params["SearchTerm"] = search_term
    return _request("GET", "/Trailers", params)


# ============ Years ============

def get_years(start_index: Optional[int] = None,
             limit: Optional[int] = None) -> Dict:
    """Gets production years"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    return _request("GET", "/Years", params)


# ============ Features ============

def get_features() -> Dict:
    """Gets installed features"""
    return _request("GET", "/Features")


# ============ UI ============

def get_ui_views(start_index: Optional[int] = None,
                limit: Optional[int] = None) -> Dict:
    """Gets UI views"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    return _request("GET", "/UI/Views", params)


def post_ui_command(command: str, **kwargs) -> Dict:
    """Executes UI command"""
    data = {"Command": command}
    data.update({k: v for k, v in kwargs.items() if v is not None})
    return _request("POST", "/UI/Command", data=data)


# ============ Videos ============

def merge_video_versions(item_ids: List[str]) -> Dict:
    """Merges video versions"""
    data = {"ItemIds": item_ids}
    return _request("POST", "/Videos/MergeVersions", data=data)


def delete_active_video_encodings(close_encodings: bool = True) -> Dict:
    """Deletes active video encodings"""
    params = {"CloseEncodings": close_encodings}
    return _request("DELETE", "/Videos/ActiveEncodings", params)


# ============ Web ============

def get_web_configuration_page(name: str) -> Dict:
    """Gets configuration page"""
    params = {"Name": name}
    return _request("GET", "/web/ConfigurationPage", params)


def get_web_configuration_pages() -> Dict:
    """Gets configuration pages"""
    return _request("GET", "/web/ConfigurationPages")


def get_web_strings(culture: Optional[str] = None) -> Dict:
    """Gets web strings"""
    params = {}
    if culture: params["Culture"] = culture
    return _request("GET", "/web/strings", params)


def get_web_string_set(culture: Optional[str] = None) -> Dict:
    """Gets web string set"""
    params = {}
    if culture: params["Culture"] = culture
    return _request("GET", "/web/stringset", params)


# ============ OpenAPI ============

def get_openapi() -> Dict:
    """Gets OpenAPI spec"""
    return _request("GET", "/openapi")


def get_openapi_json() -> Dict:
    """Gets OpenAPI JSON"""
    return _request("GET", "/openapi.json")


def get_swagger() -> Dict:
    """Gets Swagger spec"""
    return _request("GET", "/swagger")


def get_swagger_json() -> Dict:
    """Gets Swagger JSON"""
    return _request("GET", "/swagger.json")


# ============ Playback ============

def get_video_stream_url(item_id: str, media_source_id: Optional[str] = None,
                        profile: Optional[str] = None,
                        play_session_id: Optional[str] = None,
                        max_streaming_bitrate: Optional[int] = None,
                        audio_stream_index: Optional[int] = None,
                        subtitle_stream_index: Optional[int] = None,
                        start_time_ticks: Optional[int] = None,
                        transcoding_container: Optional[str] = None,
                        transcoding_protocol: Optional[str] = None) -> Response:
    """Gets video stream URL (returns stream response)"""
    params = {"api_key": API_KEY}
    if media_source_id: params["MediaSourceId"] = media_source_id
    if profile: params["Profile"] = profile
    if play_session_id: params["PlaySessionId"] = play_session_id
    if max_streaming_bitrate: params["MaxStreamingBitrate"] = max_streaming_bitrate
    if audio_stream_index is not None: params["AudioStreamIndex"] = audio_stream_index
    if subtitle_stream_index is not None: params["SubtitleStreamIndex"] = subtitle_stream_index
    if start_time_ticks: params["StartTimeTicks"] = start_time_ticks
    if transcoding_container: params["TranscodingContainer"] = transcoding_container
    if transcoding_protocol: params["TranscodingProtocol"] = transcoding_protocol
    
    url = f"{BASE_URL}/Videos/{item_id}/stream"
    return requests.get(url, params=params, stream=True)


def download_video(item_id: str, output_path: str = None,
                  media_source_id: Optional[str] = None,
                  play_session_id: Optional[str] = None,
                  max_streaming_bitrate: Optional[int] = None) -> bytes:
    """Downloads video to file or returns bytes"""
    resp = get_video_stream_url(item_id, media_source_id, 
                                play_session_id=play_session_id,
                                max_streaming_bitrate=max_streaming_bitrate)
    if output_path:
        with open(output_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return None
    return resp.content


def get_audio_stream_url(item_id: str, media_source_id: Optional[str] = None,
                        profile: Optional[str] = None,
                        play_session_id: Optional[str] = None,
                        max_streaming_bitrate: Optional[int] = None,
                        audio_stream_index: Optional[int] = None,
                        start_time_ticks: Optional[int] = None,
                        transcoding_container: Optional[str] = None,
                        transcoding_protocol: Optional[str] = None) -> Response:
    """Gets audio stream URL (returns stream response)"""
    params = {"api_key": API_KEY}
    if media_source_id: params["MediaSourceId"] = media_source_id
    if profile: params["Profile"] = profile
    if play_session_id: params["PlaySessionId"] = play_session_id
    if max_streaming_bitrate: params["MaxStreamingBitrate"] = max_streaming_bitrate
    if audio_stream_index is not None: params["AudioStreamIndex"] = audio_stream_index
    if start_time_ticks: params["StartTimeTicks"] = start_time_ticks
    if transcoding_container: params["TranscodingContainer"] = transcoding_container
    if transcoding_protocol: params["TranscodingProtocol"] = transcoding_protocol
    
    url = f"{BASE_URL}/Audio/{item_id}/stream"
    return requests.get(url, params=params, stream=True)


def download_audio(item_id: str, output_path: str = None,
                  media_source_id: Optional[str] = None,
                  play_session_id: Optional[str] = None) -> bytes:
    """Downloads audio to file or returns bytes"""
    resp = get_audio_stream_url(item_id, media_source_id, play_session_id=play_session_id)
    if output_path:
        with open(output_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return None
    return resp.content


# ============ Hubs ============

def get_hub_items(hub_type: str, start_index: Optional[int] = None,
                 limit: Optional[int] = None) -> Dict:
    """Gets hub items"""
    params = {}
    if start_index is not None: params["StartIndex"] = start_index
    if limit is not None: params["Limit"] = limit
    return _request("GET", f"/Hubs/{hub_type}/Items", params)


# ============ Search ============

def search_legacy(query: str, media_type: Optional[str] = None,
                 limit: Optional[int] = None) -> Dict:
    """Legacy search"""
    params = {"Query": query}
    if media_type: params["MediaType"] = media_type
    if limit: params["Limit"] = limit
    return _request("GET", "/Search", params)

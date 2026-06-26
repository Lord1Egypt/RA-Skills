#!/usr/bin/env python3
"""
Garmin Connect API Client using garth library.

Provides methods to fetch health data from Garmin Connect API.
"""

import json
import os
import sys
from datetime import date, datetime, timedelta
from typing import Optional, List, Dict, Any

try:
    import garth
except ImportError:
    print("Error: garth library not installed.", file=sys.stderr)
    print("Please install garth: pip3 install garth", file=sys.stderr)
    sys.exit(1)

from authenticate import GarminAuthClient, GarminAuthError


class GarminData:
    """Container for sleep data from Garmin Connect."""

    def __init__(self, raw_data=None):
        self.raw_data = raw_data or {}

    @property
    def sleep_time_seconds(self) -> int:
        return self.raw_data.get('sleepTimeSeconds', 0)

    @property
    def deep_sleep_seconds(self) -> int:
        return self.raw_data.get('deepSleepSeconds', 0)

    @property
    def light_sleep_seconds(self) -> int:
        return self.raw_data.get('lightSleepSeconds', 0)

    @property
    def rem_sleep_seconds(self) -> int:
        return self.raw_data.get('remSleepSeconds', 0)

    @property
    def sleep_scores(self) -> Dict[str, Any]:
        return self.raw_data.get('sleepScores', {})

    @property
    def overall_sleep_score(self) -> Optional[int]:
        overall = self.sleep_scores.get('overall', {})
        return overall.get('value') if overall else None

    @property
    def sleep_qualifier(self) -> Optional[str]:
        overall = self.sleep_scores.get('overall', {})
        return overall.get('qualifierKey') if overall else None

    @property
    def avg_overnight_hrv(self) -> Optional[int]:
        return self.raw_data.get('avgOvernightHrv')


class StepsData:
    """Container for steps data from Garmin Connect."""

    def __init__(self, raw_data=None):
        self.raw_data = raw_data or {}

    @property
    def total_steps(self) -> int:
        return self.raw_data.get('totalSteps', 0)

    @property
    def step_goal(self) -> int:
        return self.raw_data.get('stepGoal', 10000)

    @property
    def total_distance_meters(self) -> float:
        return self.raw_data.get('totalDistanceMeters', 0)

    @property
    def floors_ascended(self) -> float:
        return self.raw_data.get('floorsAscended', 0)


class HeartRateData:
    """Container for heart rate data from Garmin Connect."""

    def __init__(self, raw_data=None):
        self.raw_data = raw_data or {}

    @property
    def resting_heart_rate(self) -> Optional[int]:
        return self.raw_data.get('restingHeartRate')


class Activity:
    """Container for activity data from Garmin Connect."""

    def __init__(self, raw_data=None):
        self.raw_data = raw_data or {}

    @property
    def activity_type(self) -> str:
        act_type = self.raw_data.get('activityType', {})
        return act_type.get('typeKey', '') if act_type else ''

    @property
    def activity_name(self) -> str:
        return self.raw_data.get('activityName', '')

    @property
    def distance_meters(self) -> float:
        return self.raw_data.get('distanceMeters', 0)

    @property
    def duration_seconds(self) -> int:
        # API returns 'duration' (in seconds), not 'durationSeconds'
        return self.raw_data.get('duration', 0) if self.raw_data.get('duration') else self.raw_data.get('durationSeconds', 0)

    @property
    def start_time(self) -> Optional[datetime]:
        time_str = self.raw_data.get('startTimeLocal')
        if time_str:
            try:
                return datetime.fromisoformat(time_str.replace('Z', '+00:00'))
            except:
                return None
        return None

    @property
    def avg_heart_rate(self) -> Optional[int]:
        return self.raw_data.get('averageHR')

    @property
    def max_heart_rate(self) -> Optional[int]:
        return self.raw_data.get('maxHR')

    @property
    def training_effect_label(self) -> Optional[str]:
        training_effect = self.raw_data.get('trainingEffect', {})
        if training_effect:
            effect_type = training_effect.get('effectType', {})
            return effect_type.get('typeKey') if effect_type else None
        return None


class GarminClient:
    """Garmin Connect API client using garth library."""

    # API base URLs
    WELLNESS_SERVICE = "wellness-service/wellness"
    DAILY_SUMMARY_SERVICE = "wellness-service/wellness"
    USERPROFILE_SERVICE = "userprofile-service/userprofile"

    def __init__(self, config_dir: str = None):
        """
        Initialize Garmin Connect client.

        Args:
            config_dir: Directory containing authentication tokens.
                       Defaults to ~/.garmin-health-report
        """
        self.auth = GarminAuthClient(config_dir)
        self.username = None

        # Load authentication (safely check if auth object exists)
        try:
            if self.auth and self.auth.is_authenticated():
                self._load_username()
        except Exception:
            # If auth check fails, just continue without loading username
            pass

    def _load_username(self):
        """Load username from garth client."""
        try:
            self.username = garth.client.username
        except Exception:
            self.username = "unknown"

    def _get_username(self) -> str:
        """Get username for API endpoints that require it."""
        if self.username is None:
            self._load_username()
        return self.username if self.username else "me"

    def _make_api_request(self, endpoint: str) -> Optional[Dict]:
        """
        Make an authenticated API request.

        Args:
            endpoint: API endpoint path (including query parameters)

        Returns:
            Response data or None if failed
        """
        try:
            self.auth.ensure_authenticated()
            response = garth.client.connectapi(endpoint)

            # Handle different response types
            if response is None:
                return None

            # If it's a dict with data key, extract it
            if isinstance(response, dict):
                if 'dailySleepDTO' in response:
                    return response['dailySleepDTO']
                elif 'userProfile' in response:
                    return response['userProfile']
                elif 'dailySummary' in response:
                    return response['dailySummary']
                elif 'summary' in response:
                    return response['summary']
                else:
                    return response

            return response

        except Exception as e:
            print(f"Warning: API request failed to {endpoint}: {e}", file=sys.stderr)
            return None

    @classmethod
    def from_saved_tokens(cls, config_dir: str = None) -> 'GarminClient':
        """
        Create a GarminClient from saved authentication tokens.

        Args:
            config_dir: Directory containing authentication tokens.

        Returns:
            GarminClient instance if authenticated, None otherwise.

        Raises:
            GarminAuthError: If no valid tokens found
        """
        client = cls(config_dir)
        try:
            if not client.is_authenticated():
                raise GarminAuthError(
                    "No valid authentication found. Run 'python3 authenticate.py' first."
                )
        except (AttributeError, TypeError):
            # If is_authenticated() check fails, assume not authenticated
            raise GarminAuthError(
                "No valid authentication found. Run 'python3 authenticate.py' first."
            )
        return client

    def is_authenticated(self) -> bool:
        """Check if client is authenticated."""
        return self.auth.is_authenticated()

    def get_user_profile(self) -> Optional[Dict[str, Any]]:
        """
        Get user profile information.

        Returns:
            Dictionary containing user profile data, or None if not available.
        """
        try:
            response = self._make_api_request(f"{self.USERPROFILE_SERVICE}/userProfile")

            if response:
                return {
                    'username': self._get_username(),
                    'displayName': response.get('displayName'),
                    # Extract other fields as needed
                }

        except Exception as e:
            print(f"Warning: Failed to get user profile: {e}", file=sys.stderr)

        return None

    def get_sleep(self, target_date: date = None) -> GarminData:
        """
        Get sleep data for a specific date.

        Args:
            target_date: Date to fetch sleep data for. Defaults to today.

        Returns:
            GarminData object containing sleep information.
        """
        if target_date is None:
            target_date = date.today()

        date_str = target_date.strftime('%Y-%m-%d')
        username = self._get_username()

        # Build API endpoint
        endpoint = (f"{self.WELLNESS_SERVICE}/dailySleepData/{username}?"
                   f"nonSleepBufferMinutes=60&date={date_str}")

        # Make API request
        response = self._make_api_request(endpoint)

        if response:
            return GarminData(response)

        # Return empty data if no response
        return GarminData({})

    def get_steps(self, target_date: date = None) -> StepsData:
        """
        Get steps data for a specific date.

        Uses garth's stats API (works in China region).

        Args:
            target_date: Date to fetch steps data for. Defaults to today.

        Returns:
            StepsData object containing steps information.
        """
        if target_date is None:
            target_date = date.today()

        date_str = target_date.strftime('%Y-%m-%d')

        # Use garth's stats steps API (works in China region)
        try:
            endpoint = f"usersummary-service/stats/steps/daily/{date_str}/{date_str}"
            response = garth.client.connectapi(endpoint)

            if isinstance(response, list) and len(response) > 0:
                data = response[0]
                return StepsData({
                    'totalSteps': data.get('totalSteps', 0),
                    'stepGoal': data.get('stepGoal', 10000),
                    'totalDistanceMeters': data.get('totalDistance', 0),
                    'floorsAscended': 0  # Not available in this API
                })
        except Exception as e:
            print(f"Warning: Failed to get steps from stats API: {e}", file=sys.stderr)

        # Return empty data if no response
        return StepsData({})

    def get_heart_rate(self, target_date: date = None) -> HeartRateData:
        """
        Get heart rate data for a specific date.

        Note: Resting HR API is not available in China region.
        This method uses avg heart rate from sleep data as a proxy.

        Args:
            target_date: Date to fetch HR data for. Defaults to today.

        Returns:
            HeartRateData object containing HR information.
        """
        if target_date is None:
            target_date = date.today()

        date_str = target_date.strftime('%Y-%m-%d')
        username = self._get_username()

        # Get sleep data (which contains avg heart rate)
        endpoint = (f"{self.WELLNESS_SERVICE}/dailySleepData/{username}?"
                   f"nonSleepBufferMinutes=60&date={date_str}")

        # Make API request
        response = self._make_api_request(endpoint)

        if response:
            # Use avgHeartRate from sleep data as proxy for resting HR
            avg_hr = response.get('avgHeartRate')
            if avg_hr:
                return HeartRateData({
                    'restingHeartRate': int(avg_hr)
                })

        # Return empty data if no response
        return HeartRateData({})

    def get_activities(self, start_date: date = None, end_date: date = None,
                     limit: int = 50) -> List[Activity]:
        """
        Get activities for a date range.

        Args:
            start_date: Start date (inclusive). Defaults to today.
            end_date: End date (inclusive). Defaults to start_date.
            limit: Maximum number of activities to return.

        Returns:
            List of Activity objects.
        """
        if start_date is None:
            start_date = date.today()
        if end_date is None:
            end_date = start_date

        # Format dates for API
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')

        # Build API endpoint with query parameters
        endpoint = (f"activitylist-service/activities/search/activities?"
                  f"startDate={start_str}&endDate={end_str}&limit={limit}")

        # Make API request
        try:
            response = garth.client.connectapi(endpoint)
        except Exception as e:
            print(f"Warning: Failed to get activities: {e}", file=sys.stderr)
            return []

        activities = []
        if response and isinstance(response, list):
            for item in response:
                try:
                    activities.append(Activity(item))
                except Exception:
                    pass

        return activities


def _demo_fetch():
    """Demo function to test the client."""
    print("Garmin Connect Client Demo")
    print("=" * 40)

    # Create client (requires authentication)
    try:
        client = GarminClient.from_saved_tokens()
    except GarminAuthError as e:
        print(f"Error: {e}")
        print("Please run 'python3 authenticate.py' first to authenticate.")
        return

    # Fetch some data
    today = date.today()
    print(f"\nFetching data for {today}...")

    sleep_data = client.get_sleep(today)
    steps_data = client.get_steps(today)
    hr_data = client.get_heart_rate(today)
    activities = client.get_activities(today)

    print(f"\nSleep: {sleep_data.sleep_time_seconds / 3600:.1f} hours")
    print(f"Steps: {steps_data.total_steps}")
    print(f"Resting HR: {hr_data.resting_heart_rate} bpm")
    print(f"Activities: {len(activities)}")


if __name__ == "__main__":
    _demo_fetch()

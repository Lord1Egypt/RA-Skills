#!/usr/bin/env python3
"""Create a scheduled Google Calendar event with OPEN access Meet space.

Workflow:
1. Create Calendar event with Meet conference (Calendar API)
2. Get meeting code from conferenceData
3. Look up Meet space using meeting code alias (Meet API spaces.get)
4. Patch Meet space to set accessType=OPEN (Meet API spaces.patch)

Required packages:
    pip install google-auth google-auth-oauthlib google-api-python-client
"""

import os
import sys
import json
import pickle
import argparse
from datetime import datetime, timedelta

# Check for required packages
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError as e:
    print("❌ Error: Required packages not found.")
    print("\nPlease install the required packages:")
    print("    pip install google-auth google-auth-oauthlib google-api-python-client")
    print("\nOr run:")
    print("    pip install -r requirements.txt")
    sys.exit(1)

# Scopes for both Calendar and Meet APIs
# Using meetings.space.settings (non-sensitive) instead of meetings.space.created (sensitive)
SCOPES = [
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/meetings.space.settings'
]

def get_client_config_from_file(credentials_path):
    """Load client config from a JSON file."""
    if not os.path.exists(credentials_path):
        return None
    
    with open(credentials_path, 'r') as f:
        config = json.load(f)
    
    if 'installed' in config:
        return config
    elif 'web' in config:
        return config
    elif 'client_id' in config and 'client_secret' in config:
        return {
            "installed": {
                "client_id": config["client_id"],
                "client_secret": config["client_secret"],
                "auth_uri": config.get("auth_uri", "https://accounts.google.com/o/oauth2/auth"),
                "token_uri": config.get("token_uri", "https://oauth2.googleapis.com/token"),
                "redirect_uris": config.get("redirect_uris", ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"])
            }
        }
    
    return None

def get_client_config_from_env():
    """Load client config from environment variables."""
    client_id = os.environ.get('GOOGLE_CLIENT_ID')
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        return None
    
    return {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
        }
    }

def get_client_config(args):
    """Get client config from various sources."""
    
    if args.credentials:
        config = get_client_config_from_file(args.credentials)
        if config:
            return config
        else:
            raise ValueError(f"Invalid credentials file: {args.credentials}")
    
    config = get_client_config_from_env()
    if config:
        return config
    
    default_paths = [
        'client_secrets.json',
        'credentials.json',
        os.path.expanduser('~/.config/google-meet/client_secrets.json'),
        os.path.expanduser('~/.config/google-meet/credentials.json'),
    ]
    
    for path in default_paths:
        config = get_client_config_from_file(path)
        if config:
            return config
    
    raise FileNotFoundError(
        "Google OAuth credentials not found.\n\n"
        "Please provide credentials using one of these methods:\n"
        "1. Set environment variables:\n"
        "   export GOOGLE_CLIENT_ID='your-client-id'\n"
        "   export GOOGLE_CLIENT_SECRET='your-client-secret'\n\n"
        "2. Provide a credentials file:\n"
        "   python book_meeting.py --credentials /path/to/client_secrets.json\n\n"
        "3. Place client_secrets.json in the current directory\n\n"
        "To get credentials:\n"
        "1. Go to https://console.cloud.google.com/apis/credentials\n"
        "2. Create OAuth 2.0 credentials (Desktop app type)\n"
        "3. Download the JSON file\n"
        "4. Enable Google Calendar API and Google Meet API"
    )

def get_credentials(client_config, token_path='meeting_token.pickle'):
    """Get valid user credentials from storage."""
    creds = None

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            # prompt='consent' forces the consent screen to show every time
            # This allows switching to a different Google account
            creds = flow.run_local_server(port=0, prompt='consent')

        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def create_calendar_event_with_meet(service, title, start_time, end_time, timezone, 
                                     attendees=None, description=None):
    """Create calendar event with Google Meet conference."""
    
    event_body = {
        'summary': title,
        'start': {
            'dateTime': start_time,
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_time,
            'timeZone': timezone,
        },
        'conferenceData': {
            'createRequest': {
                'requestId': f"{title}-{start_time}",
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                }
            }
        }
    }
    
    if description:
        event_body['description'] = description
    
    if attendees:
        event_body['attendees'] = [{'email': email} for email in attendees]
    
    event = service.events().insert(
        calendarId='primary',
        body=event_body,
        conferenceDataVersion=1
    ).execute()
    
    return event

def get_meet_space_by_code(creds, meeting_code):
    """Look up Meet space using meeting code alias."""

    # Use google-api-python-client for Meet API
    meet_service = build('meet', 'v2', credentials=creds)

    try:
        # Try using meeting code as alias: spaces/{meetingCode}
        # The meeting code should be formatted without hyphens for the API
        clean_code = meeting_code.replace('-', '')
        print(f"   Trying to look up space with code: {clean_code}")
        space = meet_service.spaces().get(name=f'spaces/{clean_code}').execute()
        return space
    except HttpError as e:
        error_details = e._get_reason()
        print(f"   Error looking up space: {error_details}")
        print(f"   Full error: {e}")
        raise Exception(f"Meet API Error {e.resp.status}: {error_details}")

def patch_meet_space_access_type(creds, space_name, access_type='OPEN'):
    """Patch Meet space to set accessType.
    
    Must use the real resource name (spaces/{space}), not the meeting-code alias.
    """
    
    # Use google-api-python-client for Meet API
    meet_service = build('meet', 'v2', credentials=creds)
    
    patch_body = {
        "config": {
            "accessType": access_type,
            "entryPointAccess": "ALL"
        }
    }
    
    try:
        space = meet_service.spaces().patch(name=space_name, body=patch_body).execute()
        return space
    except HttpError as e:
        raise Exception(f"Meet API Error {e.resp.status}: {e._get_reason()}")

def parse_datetime(date_str, time_str):
    """Parse date and time strings."""
    # Parse date
    for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y']:
        try:
            date_obj = datetime.strptime(date_str, fmt)
            break
        except ValueError:
            continue
    else:
        raise ValueError(f"Invalid date format: {date_str}")
    
    # Parse time
    time_str = time_str.strip().upper()
    for fmt in ['%H:%M', '%I:%M %p', '%I:%M%p']:
        try:
            time_obj = datetime.strptime(time_str, fmt)
            break
        except ValueError:
            continue
    else:
        raise ValueError(f"Invalid time format: {time_str}")
    
    # Combine
    start_datetime = date_obj.replace(
        hour=time_obj.hour,
        minute=time_obj.minute,
        second=0,
        microsecond=0
    )
    
    return start_datetime

def print_meeting_details(event, space):
    """Print meeting details."""
    
    conference_data = event.get('conferenceData', {})
    entry_points = conference_data.get('entryPoints', [])
    
    meet_url = None
    meeting_code = None
    
    for ep in entry_points:
        if ep.get('entryPointType') == 'video':
            meet_url = ep.get('uri')
            meeting_code = ep.get('meetingCode')
            break
    
    print("\n" + "="*60)
    print("✅ Meeting created successfully!")
    print("="*60)
    print(f"\n📅 Title: {event.get('summary')}")
    print(f"🕐 Start: {event['start'].get('dateTime')}")
    print(f"🕐 End: {event['end'].get('dateTime')}")
    print(f"🌐 Timezone: {event['start'].get('timeZone')}")
    
    if meet_url:
        print(f"\n🔗 Meet URL: {meet_url}")
        print(f"📞 Meeting Code: {meeting_code}")
    
    if space:
        print(f"🔓 Access Type: {space.get('config', {}).get('accessType', 'N/A')}")
        print(f"🆔 Space Name: {space.get('name')}")
    
    print(f"\n📧 Calendar Link: {event.get('htmlLink')}")
    print(f"🆔 Event ID: {event.get('id')}")
    print("="*60)

def main():
    parser = argparse.ArgumentParser(
        description='Create a scheduled Google Calendar event with OPEN access Meet space.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create meeting at 8 PM New York time
  python book_meeting.py --title "MyMeet" --date "2026-03-11" --time "20:00" \\
    --duration 45 --timezone "America/New_York"
  
  # With attendees
  python book_meeting.py --title "Team Meeting" --date "2026-03-11" --time "20:00" \\
    --duration 45 --timezone "America/New_York" \\
    --attendees "user1@example.com,user2@example.com"
        """
    )
    
    parser.add_argument('--title', '-t', required=True, help='Meeting title')
    parser.add_argument('--date', '-d', required=True, help='Meeting date (YYYY-MM-DD or MM/DD/YYYY)')
    parser.add_argument('--time', required=True, help='Meeting start time (HH:MM)')
    parser.add_argument('--duration', type=int, default=45, help='Meeting duration in minutes (default: 45)')
    parser.add_argument('--timezone', '-z', default='America/New_York', help='Timezone (default: America/New_York)')
    parser.add_argument('--attendees', help='Comma-separated list of attendee emails')
    parser.add_argument('--description', help='Meeting description')
    parser.add_argument('--access-type', choices=['OPEN', 'TRUSTED', 'RESTRICTED'], 
                        default='OPEN', help='Meet access type (default: OPEN)')
    parser.add_argument('--credentials', '-c', help='Path to Google OAuth client secrets JSON file')
    parser.add_argument('--token-path', default='meeting_token.pickle', help='Path to store OAuth token')
    
    args = parser.parse_args()
    
    try:
        # Get credentials
        client_config = get_client_config(args)
        creds = get_credentials(client_config, args.token_path)
        
        # Build Calendar service
        calendar_service = build('calendar', 'v3', credentials=creds)
        
        # Parse datetime
        start_dt = parse_datetime(args.date, args.time)
        end_dt = start_dt + timedelta(minutes=args.duration)
        
        start_time = start_dt.strftime('%Y-%m-%dT%H:%M:%S')
        end_time = end_dt.strftime('%Y-%m-%dT%H:%M:%S')
        
        # Parse attendees
        attendees = None
        if args.attendees:
            attendees = [email.strip() for email in args.attendees.split(',')]
        
        # Step 1: Create Calendar event with Meet conference
        print(f"\n🚀 Step 1: Creating Calendar event with Meet conference...")
        event = create_calendar_event_with_meet(
            calendar_service,
            title=args.title,
            start_time=start_time,
            end_time=end_time,
            timezone=args.timezone,
            attendees=attendees,
            description=args.description
        )
        
        # Get meeting code from conference data
        conference_data = event.get('conferenceData', {})
        conference_id = conference_data.get('conferenceId')
        
        if not conference_id:
            print("❌ Failed to get meeting code from Calendar event")
            print_meeting_details(event, None)
            return
        
        print(f"✅ Calendar event created with Meet conference")
        print(f"   Meeting Code: {conference_id}")
        
        # Step 2: Look up Meet space using meeting code alias
        print(f"\n🚀 Step 2: Looking up Meet space using meeting code...")
        try:
            space = get_meet_space_by_code(creds, conference_id)
            print(f"✅ Found Meet space: {space.get('name')}")
        except Exception as e:
            print(f"⚠️  Could not look up Meet space: {e}")
            print_meeting_details(event, None)
            return
        
        # Step 3: Patch Meet space to set accessType
        print(f"\n🚀 Step 3: Patching Meet space to {args.access_type} access...")
        try:
            patched_space = patch_meet_space_access_type(creds, space.get('name'), args.access_type)
            print(f"✅ Meet space patched successfully!")
            print(f"   Access Type: {patched_space.get('config', {}).get('accessType')}")
        except Exception as e:
            print(f"⚠️  Could not patch Meet space: {e}")
            print_meeting_details(event, space)
            return
        
        # Print final meeting details
        print_meeting_details(event, patched_space)
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except HttpError as e:
        print(f"❌ Google API Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

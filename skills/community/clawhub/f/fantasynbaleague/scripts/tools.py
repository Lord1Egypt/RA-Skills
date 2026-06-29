from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def getAveragesLeagueRankings(
    order: Optional[str] = "desc"
) -> Dict[str, Any]:
    """
    
Get the average league rankings from the API.

IMPORTANT - SCORING SYSTEM EXPLANATION:
This is a ROTISSERIE (ROTO) fantasy league. Teams earn ranking points in 8 categories.

CRITICAL: Do NOT confuse "ranking points" with "rank position"!
- Category values (fg_percentage, ast, reb, etc.) = POINTS earned (higher is better)
- The "rank" field = actual position/place in standings (1 = first place)

HOW RANKING POINTS WORK:
- In each category, teams are ranked 1st to Nth (where N = number of teams)
- Best team in a category gets N points, second-best gets N-1, worst gets 1
- Example in 12-team league: 1st place = 12 pts, 2nd = 11 pts, ..., 12th = 1 pt
- total_points = sum of points from all 8 categories
- Overall "rank" is determined by total_points (highest total = rank 1)

EXAMPLE in a 12-team league:
{
    "team": {"team_name": "Best Team"},
    "ast": 12.0,           // Earned 12 pts (1st place in assists)
    "reb": 11.0,           // Earned 11 pts (2nd place in rebounds)
    "stl": 8.0,            // Earned 8 pts (5th place in steals)
    ...other categories...
    "total_points": 73.0,  // Sum of all 8 category points
    "rank": 1,             // Overall standing: 1st place
    "GP": 55               // Games played (informational only, not ranked)
}

Args:
    order: Sort order for rankings.
           - "desc" = best to worst (top teams first, "from top to bottom", "מלמעלה למטה")
           - "asc" = worst to best (bottom teams first, "from bottom to top", "מלמטה למעלה")
           Default is "desc".

Returns:
    A list of teams with their rankings, total points, and stats per category.
    Each item in the list is a dictionary with the following keys: {
        "team": {
            "team_id": <team_id>,
            "team_name": <team_name>
        },
        "fg_percentage": <ranking_points_for_field_goal_percentage>,
        "ft_percentage": <ranking_points_for_free_throw_percentage>,
        "three_pm": <ranking_points_for_three_pointers_made>,
        "ast": <ranking_points_for_assists>,
        "reb": <ranking_points_for_rebounds>,
        "stl": <ranking_points_for_steals>,
        "blk": <ranking_points_for_blocks>,
        "pts": <ranking_points_for_points>,
        "total_points": <sum_of_all_category_ranking_points>,
        "rank": <overall_position_1_is_first_place>,
        "GP": <games_played_not_ranked>
    }
    
NOTES:
- Higher values in categories = better performance (more ranking points earned)
- "rank" field is opposite: lower number = better (1 is first place)
- GP (games played) is informational only, not used in scoring
- When referring to steals in Hebrew, use חטיפות (not גניבות)
- If you refer to comparing teams, distinguish between rank and total points, so f.e someone can be 1st place 70 total points and another team can be 2nd place 69 total points.
- In that case, the difference is 2 points, not 1 place.

    
    Args:
        order: null
    
    Returns:
        
    """
    arguments = {
        "order": order
    }
    
    return call_api("1777419061332995", "getAveragesLeagueRankings", arguments)

def getTeams(
) -> Dict[str, Any]:
    """
    
Get the list of all teams in the fantasy league.

Use this endpoint to discover team IDs for use with other endpoints like getTeamDetails().

Returns:
    A list of teams with their team_id and team_name.
    Each item in the list is a dictionary with the following keys: {
        "team_id": <integer_team_identifier>,
        "team_name": <string_team_name>
    }
    
NOTES:
- Team IDs are required for getTeamDetails(team_id)
- Team names may contain emojis or special characters
- The list includes all active teams in the league

    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777419061332995", "getTeams", arguments)

def getAverageStats(
    use_normalized: Optional[bool] = False
) -> Dict[str, Any]:
    """
    
Get the average statistics (actual performance numbers) for all teams from the API.

IMPORTANT: This returns ACTUAL PERFORMANCE STATS, NOT ranking points!
- This is different from getAveragesLeagueRankings() which returns ranking points
- Use this endpoint to see actual per-game averages (e.g., 25.3 assists per game)
- Use getAveragesLeagueRankings() to see rotisserie ranking points (e.g., 12 points earned)

Args:
    use_normalized: If True, returns normalized data (0-1 scale) for comparison.
                   If False, returns raw statistical values (e.g., 45.6% FG, 12.3 AST).
                   Default is False.

Returns:
    A list of teams with their actual statistical averages per game.
    Each item in the list is a dictionary with the following structure:
    {
        "team": {
            "team_id": <team_id>,
            "team_name": <team_name>
        },
        "stats": {
            "FG%": <field_goal_percentage_as_decimal>,
            "FT%": <free_throw_percentage_as_decimal>,
            "3PM": <three_pointers_made_per_game>,
            "AST": <assists_per_game>,
            "REB": <rebounds_per_game>,
            "STL": <steals_per_game>,
            "BLK": <blocks_per_game>,
            "PTS": <points_per_game>,
            "GP": <games_played>
        }
    }
    
NOTES:
- Percentages are decimals (0.456 = 45.6%)
- All counting stats (3PM, AST, REB, STL, BLK, PTS) are per-game averages
- When use_normalized=True, all values are scaled 0-1 for heatmap visualization
- GP (games played) is a total count, not an average

    
    Args:
        use_normalized: null
    
    Returns:
        
    """
    arguments = {
        "use_normalized": use_normalized
    }
    
    return call_api("1777419061332995", "getAverageStats", arguments)

def getTeamDetails(
    team_id: int
) -> Dict[str, Any]:
    """
    
Get comprehensive details for a specific team from the API.

This endpoint combines multiple data types for a single team:
1. Raw statistical averages (actual performance numbers)
2. Ranking points (rotisserie scoring system)
3. Category ranks (position in each category, 1=best)
4. Player roster with individual stats

IMPORTANT - Understanding the Data Sections:

"raw_averages" = Actual statistical performance (e.g., 45.6% FG, 12.3 assists per game)
"ranking_stats" = Rotisserie points earned in each category (see explanation below)
"category_ranks" = Ordinal position in each category (1=1st place, 2=2nd place, etc.)
"shot_chart" = Raw totals for field goals and free throws (not averages)

RANKING STATS EXPLANATION (Same as getAveragesLeagueRankings):
This is a ROTISSERIE (ROTO) fantasy league. Teams earn ranking points in 8 categories.

CRITICAL: Do NOT confuse "ranking points" with "category ranks"!
- ranking_stats values (e.g., ast: 12.0) = POINTS earned (higher is better)
- category_ranks values (e.g., AST: 1) = position/place (lower is better, 1 = first)

HOW RANKING POINTS WORK:
- In each category, teams are ranked 1st to Nth (where N = number of teams)
- Best team in a category gets N points, second-best gets N-1, worst gets 1
- Example in 12-team league: 1st place = 12 pts, 2nd = 11 pts, ..., 12th = 1 pt
- total_points = sum of points from all 8 categories
- Overall "rank" is determined by total_points (highest total = rank 1)

Args:
    team_id: The ID of the team to get details for. Use getTeams() to see all team IDs.

Returns:
    A dictionary containing comprehensive team information: {
        "team": {
            "team_id": <team_id>,
            "team_name": <team_name>
        },
        "espn_url": <espn_team_page_url_string>,
        
        "shot_chart": {
            "team": {"team_id": <id>, "team_name": <name>},
            "fgm": <total_field_goals_made>,
            "fga": <total_field_goals_attempted>,
            "fg_percentage": <calculated_field_goal_percentage_as_decimal>,
            "ftm": <total_free_throws_made>,
            "fta": <total_free_throws_attempted>,
            "ft_percentage": <calculated_free_throw_percentage_as_decimal>,
            "gp": <games_played>
        },
        
        "raw_averages": {
            "fg_percentage": <average_field_goal_percentage_as_decimal>,
            "ft_percentage": <average_free_throw_percentage_as_decimal>,
            "three_pm": <average_three_pointers_made_per_game>,
            "ast": <average_assists_per_game>,
            "reb": <average_rebounds_per_game>,
            "stl": <average_steals_per_game>,
            "blk": <average_blocks_per_game>,
            "pts": <average_points_per_game>,
            "gp": <games_played>,
            "team": {"team_id": <id>, "team_name": <name>}
        },
        
        "ranking_stats": {
            "team": {"team_id": <id>, "team_name": <name>},
            "fg_percentage": <ranking_points_earned_in_fg_percentage>,
            "ft_percentage": <ranking_points_earned_in_ft_percentage>,
            "three_pm": <ranking_points_earned_in_three_pointers>,
            "ast": <ranking_points_earned_in_assists>,
            "reb": <ranking_points_earned_in_rebounds>,
            "stl": <ranking_points_earned_in_steals>,
            "blk": <ranking_points_earned_in_blocks>,
            "pts": <ranking_points_earned_in_points>,
            "gp": <games_played_not_ranked>,
            "total_points": <sum_of_all_8_category_ranking_points>,
            "rank": <overall_standing_1_is_first_place>
        },
        
        "category_ranks": {
            "FG%": <ranking_points_earned_in_fg_percentage>,
            "FT%": <ranking_points_earned_in_ft_percentage>,
            "3PM": <ranking_points_earned_in_three_pointers>,
            "AST": <ranking_points_earned_in_assists>,
            "REB": <ranking_points_earned_in_rebounds>,
            "STL": <ranking_points_earned_in_steals>,
            "BLK": <ranking_points_earned_in_blocks>,
            "PTS": <ranking_points_earned_in_points>
        },
        
        "players": [
            {
                "player_name": <player_full_name_string>,
                "pro_team": <nba_team_abbreviation_string>,
                "positions": <list_of_eligible_positions>,
                "stats": {
                    "pts": <average_points_per_game>,
                    "reb": <average_rebounds_per_game>,
                    "ast": <average_assists_per_game>,
                    "stl": <average_steals_per_game>,
                    "blk": <average_blocks_per_game>,
                    "fgm": <average_field_goals_made_per_game>,
                    "fga": <average_field_goals_attempted_per_game>,
                    "ftm": <average_free_throws_made_per_game>,
                    "fta": <average_free_throws_attempted_per_game>,
                    "fg_percentage": <field_goal_percentage_as_decimal>,
                    "ft_percentage": <free_throw_percentage_as_decimal>,
                    "three_pm": <average_three_pointers_made_per_game>,
                    "minutes": <average_minutes_per_game>,
                    "gp": <total_games_played>
                },
                "team_id": <fantasy_team_id>
            }
        ]
    }
    
EXAMPLE - Understanding the Different Data Types:
If a team shows:
- raw_averages.ast: 25.3 → Team averages 25.3 assists per game (actual performance)
- ranking_stats.ast: 12.0 → Team earned 12 ranking points in assists (1st place in 12-team league)
- category_ranks.AST: 1 → Team is ranked 1st in assists category

NOTES:
- Higher ranking_stats values = more points earned = better
- Lower category_ranks values = better position (1 is first place)
- raw_averages are the actual statistical performance
- GP (games played) is informational only, not used in ranking calculations
- When referring to steals in Hebrew, use חטיפות (not גניבות)

    
    Args:
        team_id: null
    
    Returns:
        
    """
    arguments = {
        "team_id": team_id
    }
    
    return call_api("1777419061332995", "getTeamDetails", arguments)

def getLeagueShotsStats(
) -> Dict[str, Any]:
    """
    
Get league-wide shooting statistics (field goals and free throws) for all teams.

This endpoint provides CUMULATIVE TOTALS (not per-game averages) for shooting stats.
Useful for understanding overall team shooting efficiency across the season.

Returns:
    A dictionary containing league-wide shooting statistics: {
        "shots": [
            {
                "team": {
                    "team_id": <team_id>,
                    "team_name": <team_name>
                },
                "fgm": <total_field_goals_made>,
                "fga": <total_field_goals_attempted>,
                "fg_percentage": <calculated_field_goal_percentage_as_decimal>,
                "ftm": <total_free_throws_made>,
                "fta": <total_free_throws_attempted>,
                "ft_percentage": <calculated_free_throw_percentage_as_decimal>,
                "gp": <games_played>
            }
        ]
    }

NOTES:
- fgm, fga, ftm, fta are TOTALS across all games, not per-game averages
- fg_percentage and ft_percentage are calculated from totals (fgm/fga, ftm/fta)
- Percentages are returned as decimals (e.g., 0.456 = 45.6%)
- The list contains one entry per team with their complete shooting profile

    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777419061332995", "getLeagueShotsStats", arguments)


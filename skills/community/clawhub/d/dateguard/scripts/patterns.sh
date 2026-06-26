#!/usr/bin/env bash
# DateGuard -- Date/Time Anti-Pattern Definitions
# 90 patterns across 6 categories, 15 patterns each.
#
# Format per line:
#   REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Severity levels:
#   critical -- Data corruption or security vulnerability from date handling
#   high     -- Significant date/time bug that will cause incorrect behavior
#   medium   -- Moderate concern that should be addressed
#   low      -- Best practice suggestion
#
# IMPORTANT: All regexes use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [[:alnum:]] instead of \w
# - NEVER use pipe (|) for alternation inside regex -- it conflicts with
#   the field delimiter. Use separate patterns or character classes instead.

set -euo pipefail

# ===========================================================================
# TZ -- Timezone Handling (15 patterns: TZ-001 to TZ-015)
# Free tier
# ===========================================================================

declare -a DATEGUARD_TZ_PATTERNS=(
  'datetime\.now\(\)|high|TZ-001|datetime.now() returns local time without timezone info|Use datetime.now(timezone.utc) or datetime.now(tz=ZoneInfo("UTC"))'
  'new[[:space:]]+Date\(\)|medium|TZ-002|new Date() returns local time which varies by environment|Use new Date().toISOString() or explicit UTC methods'
  'Date\.now\(\)|low|TZ-003|Date.now() returns UTC milliseconds -- ensure consistent interpretation|Document that Date.now() returns UTC epoch milliseconds'
  'datetime\.utcnow\(\)|high|TZ-004|datetime.utcnow() returns naive datetime without tzinfo|Use datetime.now(timezone.utc) instead of utcnow()'
  'getTimezoneOffset|low|TZ-005|getTimezoneOffset varies by client -- do not use for server logic|Handle timezone conversion server-side with IANA timezone database'
  'timezone[[:space:]]*=[[:space:]]*["\x27]UTC[+\-][0-9]|high|TZ-006|Hardcoded UTC offset ignores DST changes|Use IANA timezone names like America/New_York instead of UTC offsets'
  'setHours\([[:space:]]*0[[:space:]]*,[[:space:]]*0[[:space:]]*,[[:space:]]*0|medium|TZ-007|Setting time to midnight in local timezone may cross date boundary|Use UTC methods or specify timezone explicitly for date boundaries'
  'replace\([[:space:]]*tzinfo[[:space:]]*=|high|TZ-008|Replacing tzinfo directly can produce invalid times during DST|Use localize() or ZoneInfo for proper timezone conversion'
  'pytz\.timezone|low|TZ-009|pytz is legacy; consider migrating to zoneinfo (Python 3.9+)|Use zoneinfo.ZoneInfo for timezone handling in Python 3.9+'
  'moment\(\)|low|TZ-010|Moment.js is deprecated; use modern alternatives|Migrate to date-fns, Luxon, or Temporal API'
  'strftime\([[:space:]]*["\x27]%Z|medium|TZ-011|%Z timezone abbreviation is ambiguous (CST could be US or China)|Use %z for numeric offset or store IANA timezone name separately'
  'astimezone\(\)|medium|TZ-012|astimezone() without argument uses system local timezone|Pass explicit timezone argument to astimezone(tz)'
  'TimeZone\.getDefault|medium|TZ-013|JVM default timezone changes at runtime and across environments|Pass explicit timezone to all date operations instead of using default'
  'LocalDateTime\.now\(\)|high|TZ-014|LocalDateTime has no timezone info -- unsuitable for distributed systems|Use ZonedDateTime or OffsetDateTime for timezone-aware operations'
  'SimpleDateFormat|medium|TZ-015|SimpleDateFormat is not thread-safe and often misconfigured|Use DateTimeFormatter (Java 8+) with explicit timezone'
)

# ===========================================================================
# NF -- Naive Formatting (15 patterns: NF-001 to NF-015)
# Free tier
# ===========================================================================

declare -a DATEGUARD_NF_PATTERNS=(
  'MM/dd/yyyy|medium|NF-001|US date format MM/dd/yyyy is ambiguous internationally|Use ISO 8601 format yyyy-MM-dd for unambiguous dates'
  'dd/MM/yyyy|medium|NF-002|European date format dd/MM/yyyy is ambiguous in US context|Use ISO 8601 format yyyy-MM-dd for unambiguous dates'
  'strftime\([[:space:]]*["\x27]%m/%d/%Y|medium|NF-003|US-specific date format in strftime|Use ISO 8601 format %Y-%m-%d for storage and interchange'
  'strftime\([[:space:]]*["\x27]%d/%m/%Y|medium|NF-004|European date format in strftime|Use ISO 8601 format %Y-%m-%d for storage and interchange'
  'toLocaleDateString\(\)|medium|NF-005|toLocaleDateString() varies by runtime locale|Pass explicit locale and options: toLocaleDateString("en-US", options)'
  'toString\(\).*[Dd]ate|low|NF-006|Date.toString() produces implementation-specific format|Use toISOString() or Intl.DateTimeFormat for consistent output'
  'format\([[:space:]]*["\x27]yyyy-mm-dd|high|NF-007|Lowercase mm is minutes not months -- use MM for months|Use yyyy-MM-dd (uppercase MM) for month formatting'
  'format\([[:space:]]*["\x27]YYYY|medium|NF-008|YYYY is ISO week year, not calendar year in some libraries|Use yyyy for calendar year; YYYY only for ISO week dates'
  'date[[:space:]]*+[[:space:]]*["\x27][[:space:]]*["\x27]|low|NF-009|String concatenation for date formatting is fragile|Use date formatting library for consistent output'
  'new[[:space:]]+Intl\.DateTimeFormat\(\)|low|NF-010|DateTimeFormat without locale uses system default|Pass explicit locale to Intl.DateTimeFormat for consistent formatting'
  'DD-MM-YYYY|medium|NF-011|DD-MM-YYYY format is ambiguous -- could be confused with MM-DD-YYYY|Use ISO 8601 YYYY-MM-DD format for unambiguous dates'
  'dateFormat[[:space:]]*=[[:space:]]*["\x27][MDYmdyHhsS/\-]+["\x27]|low|NF-012|Hardcoded date format string may not work across locales|Use ISO 8601 or locale-aware formatting for international support'
  'getMonth\(\)|medium|NF-013|getMonth() returns 0-indexed (0=Jan) -- common off-by-one source|Remember getMonth() is 0-based; add 1 for display'
  'getYear\(\)|high|NF-014|getYear() is deprecated and returns years since 1900|Use getFullYear() instead of getYear()'
  'toGMTString\(\)|medium|NF-015|toGMTString() is deprecated|Use toUTCString() or toISOString() instead'
)

# ===========================================================================
# EP -- Epoch & Precision (15 patterns: EP-001 to EP-015)
# Pro tier
# ===========================================================================

declare -a DATEGUARD_EP_PATTERNS=(
  'int\([[:space:]]*time\.time\(\)|medium|EP-001|Casting epoch to int loses sub-second precision|Keep float precision or use time_ns() for nanoseconds'
  '2147483647|critical|EP-002|Magic number 2147483647 is Y2K38 max -- 32-bit time_t overflow|Use 64-bit timestamps to avoid Y2038 overflow'
  'timestamp[[:space:]]*=[[:space:]]*[0-9]{10}[[:space:]]*$|low|EP-003|Hardcoded epoch seconds may cause issues after Y2K38|Use dynamic timestamp generation; avoid hardcoded epoch values'
  'Math\.floor\([[:space:]]*Date\.now\(\)[[:space:]]*/[[:space:]]*1000|low|EP-004|Converting JS milliseconds to seconds -- ensure consistency|Document whether timestamps are in seconds or milliseconds throughout'
  'time\(\)[[:space:]]*\*[[:space:]]*1000|medium|EP-005|Multiplying epoch seconds to get milliseconds may overflow in 32-bit|Use language-native millisecond epoch functions instead of multiplication'
  'timestamp[[:space:]]*>[[:space:]]*1[0-9]{12}|low|EP-006|Timestamp comparison assumes milliseconds -- verify unit consistency|Standardize on one timestamp unit (seconds or milliseconds) across codebase'
  'TIMESTAMP[[:space:]]+WITHOUT|high|EP-007|TIMESTAMP WITHOUT TIME ZONE loses timezone context in database|Use TIMESTAMP WITH TIME ZONE for timezone-aware storage'
  'INT[[:space:]]+.*timestamp|medium|EP-008|Storing timestamp as INT may overflow for 32-bit columns|Use BIGINT or native TIMESTAMP type for epoch storage'
  'from_unixtime\([[:space:]]*[[:alnum:]]|low|EP-009|from_unixtime uses server timezone for conversion|Specify timezone explicitly when converting from unix timestamp'
  'to_timestamp\([[:space:]]*[[:alnum:]]|low|EP-010|Verify to_timestamp input is in expected unit (seconds vs ms)|Document expected timestamp unit and validate input range'
  'Date\([[:space:]]*["\x27][0-9]{10}["\x27]\)|medium|EP-011|Passing epoch string to Date constructor -- may be misinterpreted|Pass numeric epoch to Date, not string: new Date(Number(epoch))'
  'Date\.parse\([[:space:]]*["\x27]|medium|EP-012|Date.parse behavior varies across browsers and engines|Use explicit parsing with known format or ISO 8601 strings'
  'mktime\(|low|EP-013|mktime uses local timezone for conversion|Specify timezone context or use timegm/calendar.timegm for UTC'
  'datetime\.fromtimestamp\([[:space:]]*[[:alnum:]]|high|EP-014|fromtimestamp uses local timezone -- varies across servers|Use datetime.fromtimestamp(ts, tz=timezone.utc) for UTC'
  'nano[[:space:]]*=[[:space:]]*[0-9]|low|EP-015|Hardcoded nanosecond values are fragile|Use time library functions for nanosecond precision instead of literals'
)

# ===========================================================================
# DA -- Date Arithmetic (15 patterns: DA-001 to DA-015)
# Pro tier
# ===========================================================================

declare -a DATEGUARD_DA_PATTERNS=(
  '[[:space:]]*\*[[:space:]]*24[[:space:]]*\*[[:space:]]*60[[:space:]]*\*[[:space:]]*60|high|DA-001|Manual seconds calculation (days*24*60*60) ignores DST transitions|Use timedelta or duration library that accounts for DST changes'
  '[[:space:]]*\*[[:space:]]*86400|high|DA-002|Multiplying by 86400 assumes all days are 24 hours (DST-unsafe)|Use date library for day arithmetic to handle DST correctly'
  'setDate\([[:space:]]*getDate\(\)[[:space:]]*\+|medium|DA-003|Date arithmetic with setDate may behave unexpectedly at month boundaries|Use date-fns addDays() or similar library for safe date math'
  'timedelta\([[:space:]]*days[[:space:]]*=[[:space:]]*30\)|medium|DA-004|Using 30 days as a month approximation|Use relativedelta(months=1) for accurate month arithmetic'
  'timedelta\([[:space:]]*days[[:space:]]*=[[:space:]]*365\)|medium|DA-005|Using 365 days as a year approximation ignores leap years|Use relativedelta(years=1) for accurate year arithmetic'
  'addMonths\([[:space:]]*[[:alnum:]]+[[:space:]]*,[[:space:]]*1\)|low|DA-006|Adding months to dates like Jan 31 produces inconsistent results|Document or validate end-of-month behavior for month arithmetic'
  'getDate\(\)[[:space:]]*==[[:space:]]*29|low|DA-007|Checking for day 29 -- ensure leap year logic is correct|Use date library isLeapYear() for reliable leap year checks'
  'datediff|low|DA-008|DATEDIFF behavior varies between databases|Verify DATEDIFF semantics for your specific database engine'
  'date_add\([[:space:]]*[[:alnum:]]+[[:space:]]*,[[:space:]]*INTERVAL|low|DA-009|SQL DATE_ADD -- verify behavior at month/year boundaries|Test edge cases: month-end dates, leap years, DST transitions'
  'plus\([[:space:]]*Period\.|low|DA-010|Java Period addition -- day-of-month may be adjusted|Verify end-of-month handling when adding Period to date'
  'Duration\.ofDays\(|medium|DA-011|Duration.ofDays assumes 24-hour days -- DST-unsafe|Use Period.ofDays() for calendar-day arithmetic in Java'
  'moment\(\)\.add\([[:space:]]*[0-9]+[[:space:]]*,[[:space:]]*["\x27]days|low|DA-012|Moment.js add days -- verify DST handling|Test date addition across DST transitions'
  'ChronoUnit\.DAYS\.between|low|DA-013|ChronoUnit.DAYS.between counts 24-hour periods, not calendar days|Use Period.between for calendar day differences'
  'date[[:space:]]*-[[:space:]]*date|medium|DA-014|Date subtraction semantics vary by language and type|Use explicit duration/diff functions instead of date subtraction operators'
  'floor\([[:space:]]*[[:alnum:]]*[[:space:]]*/[[:space:]]*86400|high|DA-015|Integer division by 86400 to get day count ignores DST|Use date library day-count functions that respect timezone rules'
)

# ===========================================================================
# CP -- Comparison & Parsing (15 patterns: CP-001 to CP-015)
# Team tier
# ===========================================================================

declare -a DATEGUARD_CP_PATTERNS=(
  '["\x27][0-9]{4}-[0-9]{2}-[0-9]{2}["\x27][[:space:]]*[<>=]+[[:space:]]*["\x27][0-9]{4}|medium|CP-001|String comparison of dates works for ISO 8601 but is fragile|Parse dates to proper types before comparison'
  'compareTo\([[:space:]]*["\x27][0-9]{4}|medium|CP-002|Comparing date strings lexicographically|Parse strings to date objects before comparison'
  'Date\.parse\([[:space:]]*["\x27][0-9]{1,2}/|high|CP-003|Parsing ambiguous date format with Date.parse|Use explicit parsing with ISO 8601 or specify format'
  'strptime\([[:space:]]*[[:alnum:]]+[[:space:]]*,[[:space:]]*["\x27]%m/%d|medium|CP-004|Parsing US date format -- may fail for international input|Accept ISO 8601 input or validate format explicitly'
  'new[[:space:]]+Date\([[:space:]]*["\x27][0-9]{1,2}[-/]|high|CP-005|Date constructor with DD-MM or MM-DD format is ambiguous|Use ISO 8601 format YYYY-MM-DD for the Date constructor'
  'dateutil\.parser\.parse\([[:space:]]*[[:alnum:]]|medium|CP-006|dateutil.parse is lenient and may guess incorrectly|Pass dayfirst or yearfirst parameter to avoid ambiguity'
  'LocalDate\.parse\([[:space:]]*[[:alnum:]]|low|CP-007|LocalDate.parse assumes ISO format -- verify input format|Provide explicit DateTimeFormatter if input is not ISO 8601'
  '==[[:space:]]*new[[:space:]]+Date\(|high|CP-008|Date equality comparison with == checks reference not value|Use getTime() for date equality: date1.getTime() === date2.getTime()'
  'isBefore\([[:space:]]*LocalDate\.now|low|CP-009|Comparing to now() -- timezone affects which date is current|Specify timezone explicitly when using LocalDate.now(zone)'
  'datetime\.[[:alnum:]]+[[:space:]]*<[[:space:]]*datetime\.|low|CP-010|Comparing datetimes -- ensure both have consistent timezone info|Ensure both datetimes are timezone-aware or both naive before comparison'
  'BETWEEN[[:space:]]+["\x27][0-9]{4}-[0-9]{2}-[0-9]{2}["\x27][[:space:]]+AND|medium|CP-011|SQL BETWEEN for dates may miss end-of-day records|Use >= and < next day pattern instead of BETWEEN for date ranges'
  'WHERE.*date[[:space:]]*=[[:space:]]*["\x27][0-9]{4}|medium|CP-012|Exact date match in SQL misses time portion|Use date range (>= and <) for date equality in SQL queries'
  'Instant\.parse\([[:space:]]*["\x27]|low|CP-013|Instant.parse requires trailing Z or offset|Ensure input strings have timezone designator for Instant.parse'
  'DateTimeParseException|low|CP-014|Handle DateTimeParseException for user-provided dates|Add try/catch for date parsing with user-friendly error messages'
  'tryParse[[:space:]]*\([[:space:]]*[[:alnum:]]|low|CP-015|TryParse for dates -- validate with expected format|Provide explicit format string to TryParse for predictable parsing'
)

# ===========================================================================
# ST -- Storage & Serialization (15 patterns: ST-001 to ST-015)
# Team tier
# ===========================================================================

declare -a DATEGUARD_ST_PATTERNS=(
  'VARCHAR.*date|high|ST-001|Storing dates as VARCHAR loses type safety and query optimization|Use native DATE or TIMESTAMP column type for date storage'
  'TEXT.*timestamp|high|ST-002|Storing timestamps as TEXT prevents efficient queries and validation|Use native TIMESTAMP column type for timestamp storage'
  'JSON\.stringify\([[:space:]]*[[:alnum:]]*[Dd]ate|medium|ST-003|JSON.stringify converts Date to ISO string -- may lose timezone|Store timezone separately or use ISO 8601 with offset in JSON'
  'toJSON\(\)|low|ST-004|Date.toJSON() outputs UTC ISO string -- verify this is intended|Document that serialized dates are in UTC ISO 8601 format'
  'created_at[[:space:]]+VARCHAR|high|ST-005|created_at as VARCHAR prevents date indexing and range queries|Use TIMESTAMP WITH TIME ZONE for created_at columns'
  'updated_at[[:space:]]+TEXT|high|ST-006|updated_at as TEXT loses query performance and type safety|Use TIMESTAMP WITH TIME ZONE for updated_at columns'
  'serialize\([[:space:]]*[[:alnum:]]*\.[Dd]ate|low|ST-007|Custom date serialization may lose timezone info|Use ISO 8601 with offset for date serialization'
  'DATETIME[[:space:]]+DEFAULT[[:space:]]+CURRENT_TIMESTAMP|low|ST-008|DATETIME without timezone in default value|Use TIMESTAMP WITH TIME ZONE for timezone-aware defaults'
  'pickle\.dumps\([[:space:]]*[[:alnum:]]*date|medium|ST-009|Pickling date objects is fragile across Python versions|Serialize dates as ISO 8601 strings for portability'
  'Marshal\.[[:alnum:]]*\([[:space:]]*[[:alnum:]]*[Dd]ate|low|ST-010|Marshaling dates -- verify timezone is preserved|Include timezone info in marshaled date representations'
  'redis\.[[:alnum:]]*\([[:space:]]*["\x27][[:alnum:]]*date|low|ST-011|Storing dates in Redis -- use consistent format|Store dates as ISO 8601 strings or epoch milliseconds in Redis'
  'localStorage\.[[:alnum:]]*\([[:space:]]*["\x27][[:alnum:]]*date|medium|ST-012|Date in localStorage loses timezone and type info|Store dates as ISO 8601 with timezone offset in localStorage'
  'encode\([[:space:]]*[[:alnum:]]*\.[Dd]ate|low|ST-013|Encoding date -- verify format includes timezone info|Include timezone designator in all encoded date values'
  'DATETIME2|low|ST-014|DATETIME2 in SQL Server -- good precision but verify timezone handling|Consider DATETIMEOFFSET for timezone-aware storage in SQL Server'
  'writeUTF\([[:space:]]*[[:alnum:]]*\.format|medium|ST-015|Writing formatted date string -- use ISO 8601 for interchange|Use ISO 8601 format for all date serialization and interchange'
)

# ===========================================================================
# Utility Functions
# ===========================================================================

# Count total patterns
dateguard_pattern_count() {
  local count=0
  count=$((count + ${#DATEGUARD_TZ_PATTERNS[@]}))
  count=$((count + ${#DATEGUARD_NF_PATTERNS[@]}))
  count=$((count + ${#DATEGUARD_EP_PATTERNS[@]}))
  count=$((count + ${#DATEGUARD_DA_PATTERNS[@]}))
  count=$((count + ${#DATEGUARD_CP_PATTERNS[@]}))
  count=$((count + ${#DATEGUARD_ST_PATTERNS[@]}))
  echo "$count"
}

# Count patterns in a specific category
dateguard_category_count() {
  local cat="$1"
  case "$cat" in
    TZ) echo "${#DATEGUARD_TZ_PATTERNS[@]}" ;;
    NF) echo "${#DATEGUARD_NF_PATTERNS[@]}" ;;
    EP) echo "${#DATEGUARD_EP_PATTERNS[@]}" ;;
    DA) echo "${#DATEGUARD_DA_PATTERNS[@]}" ;;
    CP) echo "${#DATEGUARD_CP_PATTERNS[@]}" ;;
    ST) echo "${#DATEGUARD_ST_PATTERNS[@]}" ;;
    *)  echo "0" ;;
  esac
}

# Get the bash array name for a category code
get_dateguard_patterns_for_category() {
  local cat="$1"
  case "$cat" in
    TZ) echo "DATEGUARD_TZ_PATTERNS" ;;
    NF) echo "DATEGUARD_NF_PATTERNS" ;;
    EP) echo "DATEGUARD_EP_PATTERNS" ;;
    DA) echo "DATEGUARD_DA_PATTERNS" ;;
    CP) echo "DATEGUARD_CP_PATTERNS" ;;
    ST) echo "DATEGUARD_ST_PATTERNS" ;;
    *)  echo "" ;;
  esac
}

# Get human-readable label for a category code
get_dateguard_category_label() {
  local cat="$1"
  case "$cat" in
    TZ) echo "Timezone Handling" ;;
    NF) echo "Naive Formatting" ;;
    EP) echo "Epoch & Precision" ;;
    DA) echo "Date Arithmetic" ;;
    CP) echo "Comparison & Parsing" ;;
    ST) echo "Storage & Serialization" ;;
    *)  echo "Unknown" ;;
  esac
}

# Get space-separated list of category codes available at a given tier level.
# Tier levels: 0=free (TZ, NF), 1=pro (TZ, NF, EP, DA), 2/3=team/enterprise (all)
get_dateguard_categories_for_tier() {
  local tier_level="$1"
  case "$tier_level" in
    0) echo "TZ NF" ;;
    1) echo "TZ NF EP DA" ;;
    2|3) echo "TZ NF EP DA CP ST" ;;
    *) echo "TZ NF" ;;
  esac
}

# Severity to point deduction mapping
severity_to_points() {
  local severity="$1"
  case "$severity" in
    critical) echo 25 ;;
    high)     echo 15 ;;
    medium)   echo  8 ;;
    low)      echo  3 ;;
    *)        echo  0 ;;
  esac
}

# Validate that a string is a known category code
is_valid_dateguard_category() {
  local cat="$1"
  case "$cat" in
    TZ|NF|EP|DA|CP|ST) return 0 ;;
    *) return 1 ;;
  esac
}

# List patterns in a given category or "all"
dateguard_list_patterns() {
  local filter="${1:-all}"

  local categories="TZ NF EP DA CP ST"
  if [[ "$filter" != "all" ]]; then
    filter=$(echo "$filter" | tr '[:lower:]' '[:upper:]')
    categories="$filter"
  fi

  for cat in $categories; do
    local label
    label=$(get_dateguard_category_label "$cat")
    echo -e "${BOLD:-}--- ${cat}: ${label} ---${NC:-}"

    local arr_name
    arr_name=$(get_dateguard_patterns_for_category "$cat")
    [[ -z "$arr_name" ]] && continue

    local -n _arr="$arr_name"
    for entry in "${_arr[@]}"; do
      IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
      local sev_upper
      sev_upper=$(echo "$severity" | tr '[:lower:]' '[:upper:]')
      echo "  [$sev_upper] $check_id: $description"
    done
    echo ""
  done
}

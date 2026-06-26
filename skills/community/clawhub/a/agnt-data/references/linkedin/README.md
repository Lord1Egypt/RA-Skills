# LinkedIn API Reference

**App name:** `linkedin`
**Base URL:** `https://api.agntdata.dev/v1/data/linkedin`
**Endpoints:** 52

Enrich companies and profiles in real time. Designed for agents that need reliable structured data without managing dozens of vendor accounts.

## Authentication

All requests require the agntdata API key:

```
Authorization: Bearer $AGNTDATA_API_KEY
```

---

## Available Endpoints

| Method | Path | Summary |
|--------|------|---------|
| `GET` | `/get-company-by-domain` | Get Company By Domain |
| `GET` | `/get-company-details-by-id` | Get Company Details by ID |
| `GET` | `/get-company-details` | Get Company Details |
| `POST` | `/profiles/interests/schools` | Get Profile School Interests |
| `POST` | `/profiles/interests/newsletters` | Get Profile Newsletter Interests |
| `GET` | `/similar-profiles` | Get Similar Profiles |
| `GET` | `/profiles/position-skills` | Get Profile Positions With Skills |
| `POST` | `/profiles/interests/companies` | Get Profile Company Interest |
| `GET` | `/all-profile-data` | Profile Data & Recommendations |
| `GET` | `/get-given-recommendations` | Get Given Recommendations |
| `GET` | `/profile-data-connection-count-posts` | Get Profile Data, Connection & Follower Count and Posts |
| `GET` | `/about-this-profile` | About The Profile |
| `GET` | `/data-connection-count` | Get Profile Data and Connection & Follower Count |
| `GET` | `/get-received-recommendations` | Get Received Recommendations |
| `GET` | `/get-profile-comments` | Get Profile's Comments |
| `GET` | `/get-profile-likes` | Get Profile Reactions |
| `GET` | `/get-profile-post-and-comments` | Get Profile Post and Comments |
| `GET` | `/connection-count` | Get Profile Connection & Follower Count |
| `GET` | `/get-profile-posts-comments` | Get Profile Post Comment |
| `POST` | `/search-people-by-url` | Search People by URL |
| `GET` | `/` | Get Profile Data |
| `GET` | `/search-people` | Search People |
| `GET` | `/get-profile-data-by-url` | Get Profile Data By URL |
| `POST` | `/profiles/interests/groups` | Get Profile Group Interests |
| `POST` | `/profiles/interests/top-voices` | Get Profile Top Voice Interests |
| `GET` | `/get-profile-posts` | Get Profile's Posts |
| `POST` | `/get-post-reactions` | Get Post Reactions |
| `GET` | `/profiles/positions/top` | Get Profile Top Position |
| `GET` | `/get-company-posts` | Get Company's Post |
| `GET` | `/get-company-pages-people-also-viewed` | Get Company Pages People Also Viewed |
| `GET` | `/get-company-insights` | Get Company Insights [PREMIUM] |
| `POST` | `/search-posts` | Search Posts |
| `GET` | `/search-jobs-v2` | Search Jobs V2 |
| `GET` | `/profiles/posted-jobs` | Get Profile's Posted Jobs |
| `GET` | `/get-company-post-comments` | Get Company Post Comments |
| `POST` | `/get-company-employees-count` | Get Company Employees Count |
| `POST` | `/companies/search` | Search Companies |
| `GET` | `/get-job-details` | Get Job Details |
| `GET` | `/get-article-comments` | Get Article Comments |
| `GET` | `/get-article-reactions` | Get Article Reactions |
| `GET` | `/get-article` | Get Article |
| `GET` | `/get-user-articles` | Get User Articles |
| `POST` | `/posts/reposts` | Get Post Reposts |
| `GET` | `/get-post` | Get Post |
| `POST` | `/company-jobs` | Get Company Jobs |
| `GET` | `/search-jobs` | Search Jobs |
| `GET` | `/health` | Health Check |
| `GET` | `/get-hiring-team` | Get Hiring Team |
| `GET` | `/search-locations` | Search Locations |
| `POST` | `/search-posts-by-hashtag` | Search Post by Hashtag |
| `GET` | `/get-company-jobs-count` | Get Company Jobs Count |
| `GET` | `/get-profile-recent-activity-time` | Get Profile Recent Activity Time |

## Tool Schemas

The following JSON defines all available tools with their parameters. Each tool maps to an API endpoint.

```json
[
  {
    "name": "agntdata_linkedin_Get_Company_By_Domain",
    "description": "Get Company By Domain",
    "method": "GET",
    "path": "/get-company-by-domain",
    "parameters": {
      "type": "object",
      "properties": {
        "domain": {
          "type": "string",
          "description": "domain"
        }
      },
      "required": [
        "domain"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Company_Details_by_ID",
    "description": "Get Company Details by ID",
    "method": "GET",
    "path": "/get-company-details-by-id",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "id"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Company_Details",
    "description": "Get Company Details",
    "method": "GET",
    "path": "/get-company-details",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        }
      },
      "required": [
        "username"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Profile_School_Interests",
    "description": "Get Profile School Interests",
    "method": "POST",
    "path": "/profiles/interests/schools",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        },
        "page": {
          "type": "integer",
          "description": "page"
        }
      }
    }
  },
  {
    "name": "agntdata_linkedin_Get_Profile_Newsletter_Interests",
    "description": "Get Profile Newsletter Interests",
    "method": "POST",
    "path": "/profiles/interests/newsletters",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        },
        "page": {
          "type": "integer",
          "description": "page"
        }
      }
    }
  },
  {
    "name": "agntdata_linkedin_Get_Similar_Profiles",
    "description": "Get Similar Profiles",
    "method": "GET",
    "path": "/similar-profiles",
    "parameters": {
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "description": "url"
        }
      },
      "required": [
        "url"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Profile_Positions_With_Skills",
    "description": "Get Profile Positions With Skills",
    "method": "GET",
    "path": "/profiles/position-skills",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        }
      },
      "required": [
        "username"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Profile_Company_Interest",
    "description": "Get Profile Company Interest",
    "method": "POST",
    "path": "/profiles/interests/companies",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        },
        "page": {
          "type": "integer",
          "description": "page"
        }
      }
    }
  },
  {
    "name": "agntdata_linkedin_Profile_Data___Recommendations",
    "description": "Profile Data & Recommendations",
    "method": "GET",
    "path": "/all-profile-data",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        }
      },
      "required": [
        "username"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Given_Recommendations",
    "description": "Get Given Recommendations",
    "method": "GET",
    "path": "/get-given-recommendations",
    "parameters": {
      "type": "object",
      "properties": {
        "start": {
          "type": "string",
          "description": "start"
        },
        "username": {
          "type": "string",
          "description": "username"
        }
      },
      "required": [
        "username"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_profile_with_connections_and_posts",
    "description": "Get Profile Data, Connection & Follower Count and Posts",
    "method": "GET",
    "path": "/profile-data-connection-count-posts",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        }
      },
      "required": [
        "username"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_About_The_Profile",
    "description": "About The Profile",
    "method": "GET",
    "path": "/about-this-profile",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        }
      },
      "required": [
        "username"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_profile_with_connection_count",
    "description": "Get Profile Data and Connection & Follower Count",
    "method": "GET",
    "path": "/data-connection-count",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        }
      },
      "required": [
        "username"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Received_Recommendations",
    "description": "Get Received Recommendations",
    "method": "GET",
    "path": "/get-received-recommendations",
    "parameters": {
      "type": "object",
      "properties": {
        "start": {
          "type": "string",
          "description": "start"
        },
        "username": {
          "type": "string",
          "description": "username"
        }
      },
      "required": [
        "username"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Profile_s_Comments",
    "description": "Get Profile's Comments",
    "method": "GET",
    "path": "/get-profile-comments",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        }
      },
      "required": [
        "username"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Profile_Reactions",
    "description": "Get Profile Reactions",
    "method": "GET",
    "path": "/get-profile-likes",
    "parameters": {
      "type": "object",
      "properties": {
        "paginationToken": {
          "type": "string",
          "description": "It is required when fetching the next results page. The token from the previous call must be used."
        },
        "username": {
          "type": "string",
          "description": "username"
        },
        "start": {
          "type": "string",
          "description": "for pagination, increase +100 to parse next result until you see less than 100 results.\nit could be one of these; 0, 100, 200, 300, 400, etc."
        }
      },
      "required": [
        "username"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Profile_Post_and_Comments",
    "description": "Get Profile Post and Comments",
    "method": "GET",
    "path": "/get-profile-post-and-comments",
    "parameters": {
      "type": "object",
      "properties": {
        "urn": {
          "type": "string",
          "description": "The URN (Unique Resource Name) of the LinkedIn post. Must be a numeric URN identifier, e.g. 7181285160586211328."
        }
      },
      "required": [
        "urn"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Profile_Connection___Follower_Count",
    "description": "Get Profile Connection & Follower Count",
    "method": "GET",
    "path": "/connection-count",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        }
      },
      "required": [
        "username"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Profile_Post_Comment",
    "description": "Get Profile Post Comment",
    "method": "GET",
    "path": "/get-profile-posts-comments",
    "parameters": {
      "type": "object",
      "properties": {
        "paginationToken": {
          "type": "string",
          "description": "It is required when fetching the next results page. The token from the previous call must be used."
        },
        "page": {
          "type": "string",
          "description": "page"
        },
        "urn": {
          "type": "string",
          "description": "Post urn value"
        },
        "sort": {
          "type": "string",
          "description": "it could be one of these; mostRelevant, mostRecent"
        }
      },
      "required": [
        "urn",
        "sort"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Search_People_by_URL",
    "description": "Search People by URL",
    "method": "POST",
    "path": "/search-people-by-url",
    "parameters": {
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "description": "url"
        }
      }
    }
  },
  {
    "name": "agntdata_linkedin_Get_Profile_Data",
    "description": "Get Profile Data",
    "method": "GET",
    "path": "/",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        }
      },
      "required": [
        "username"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Search_People",
    "description": "Search People",
    "method": "GET",
    "path": "/search-people",
    "parameters": {
      "type": "object",
      "properties": {
        "firstName": {
          "type": "string",
          "description": "firstName"
        },
        "geo": {
          "type": "string",
          "description": "please follow this to find location id"
        },
        "keywordTitle": {
          "type": "string",
          "description": "keywordTitle"
        },
        "start": {
          "type": "string",
          "description": "it could be one of these; 0, 10, 20, 30, etc."
        },
        "lastName": {
          "type": "string",
          "description": "lastName"
        },
        "company": {
          "type": "string",
          "description": "Company name"
        },
        "keywordSchool": {
          "type": "string",
          "description": "keywordSchool"
        },
        "keywords": {
          "type": "string",
          "description": "keywords"
        },
        "schoolId": {
          "type": "string",
          "description": "schoolId"
        }
      }
    }
  },
  {
    "name": "agntdata_linkedin_Get_Profile_Data_By_URL",
    "description": "Get Profile Data By URL",
    "method": "GET",
    "path": "/get-profile-data-by-url",
    "parameters": {
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "description": "url"
        }
      },
      "required": [
        "url"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Profile_Group_Interests",
    "description": "Get Profile Group Interests",
    "method": "POST",
    "path": "/profiles/interests/groups",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        },
        "page": {
          "type": "integer",
          "description": "page"
        }
      }
    }
  },
  {
    "name": "agntdata_linkedin_Get_Profile_Top_Voice_Interests",
    "description": "Get Profile Top Voice Interests",
    "method": "POST",
    "path": "/profiles/interests/top-voices",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        },
        "page": {
          "type": "integer",
          "description": "page"
        }
      }
    }
  },
  {
    "name": "agntdata_linkedin_Get_Profile_s_Posts",
    "description": "Get Profile's Posts",
    "method": "GET",
    "path": "/get-profile-posts",
    "parameters": {
      "type": "object",
      "properties": {
        "start": {
          "type": "string",
          "description": "use this param to get posts in next results page: 0 for page 1, 50 for page 2 100 for page 3, etc."
        },
        "postedAt": {
          "type": "string",
          "description": "It is not an official filter. It filters posts after fetching them from LinkedIn and returns posts that are newer than the given date.\nExample value: 2024-01-01 00:00"
        },
        "username": {
          "type": "string",
          "description": "username"
        },
        "paginationToken": {
          "type": "string",
          "description": "It is required when fetching the next results page. The token from the previous call must be used."
        }
      },
      "required": [
        "username"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Post_Reactions",
    "description": "Get Post Reactions",
    "method": "POST",
    "path": "/get-post-reactions",
    "parameters": {
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "description": "url"
        },
        "page": {
          "type": "integer",
          "description": "page"
        },
        "reactionType": {
          "type": "string",
          "description": "reactionType"
        }
      }
    }
  },
  {
    "name": "agntdata_linkedin_Get_Profile_Top_Position",
    "description": "Get Profile Top Position",
    "method": "GET",
    "path": "/profiles/positions/top",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        }
      },
      "required": [
        "username"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Company_s_Post",
    "description": "Get Company's Post",
    "method": "GET",
    "path": "/get-company-posts",
    "parameters": {
      "type": "object",
      "properties": {
        "paginationToken": {
          "type": "string",
          "description": "It is required when fetching the next results page. The token from the previous call must be used."
        },
        "start": {
          "type": "string",
          "description": "use this param to get posts in next results page: 0 for page 1, 50 for page 2, 100 for page 3, etc."
        },
        "username": {
          "type": "string",
          "description": "username"
        }
      },
      "required": [
        "username"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Company_Pages_People_Also_Viewed",
    "description": "Get Company Pages People Also Viewed",
    "method": "GET",
    "path": "/get-company-pages-people-also-viewed",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        }
      }
    }
  },
  {
    "name": "agntdata_linkedin_Get_Company_Insights__PREMIUM",
    "description": "Get Company Insights [PREMIUM]",
    "method": "GET",
    "path": "/get-company-insights",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        }
      },
      "required": [
        "username"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Search_Posts",
    "description": "Search Posts",
    "method": "POST",
    "path": "/search-posts",
    "parameters": {
      "type": "object",
      "properties": {
        "keyword": {
          "type": "string",
          "description": "keyword"
        },
        "sortBy": {
          "type": "string",
          "description": "sortBy"
        },
        "datePosted": {
          "type": "string",
          "description": "datePosted"
        },
        "page": {
          "type": "integer",
          "description": "page"
        },
        "contentType": {
          "type": "string",
          "description": "contentType"
        },
        "fromMember": {
          "type": "array",
          "description": "fromMember"
        },
        "fromCompany": {
          "type": "array",
          "description": "fromCompany"
        },
        "mentionsMember": {
          "type": "array",
          "description": "mentionsMember"
        },
        "mentionsOrganization": {
          "type": "array",
          "description": "mentionsOrganization"
        },
        "authorIndustry": {
          "type": "array",
          "description": "authorIndustry"
        },
        "authorCompany": {
          "type": "array",
          "description": "authorCompany"
        },
        "authorTitle": {
          "type": "string",
          "description": "authorTitle"
        }
      }
    }
  },
  {
    "name": "agntdata_linkedin_Search_Jobs_V2",
    "description": "Search Jobs V2",
    "method": "GET",
    "path": "/search-jobs-v2",
    "parameters": {
      "type": "object",
      "properties": {
        "titleIds": {
          "type": "string",
          "description": "please follow this to find title id by title"
        },
        "salary": {
          "type": "string",
          "description": "it could be one of these; 40k+, 60k+, 80k+, 100k+, 120k+, 140k+, 160k+, 180k+, 200k+\nExample: 80k+"
        },
        "functionIds": {
          "type": "string",
          "description": "please follow this to find function id"
        },
        "companyIds": {
          "type": "string",
          "description": "please follow this to find company id"
        },
        "distance": {
          "type": "string",
          "description": "0 = 0km\n\n5 = 8km\n\n10 = 16km\n\n25 = 40km\n\n50 = 80km\n\n100 = 160km"
        },
        "experienceLevel": {
          "type": "string",
          "description": "it could be one of these; internship, associate, director, entryLevel, midSeniorLevel. executive\nexample: executive"
        },
        "locationId": {
          "type": "number",
          "description": "please follow this to find location id"
        },
        "onsiteRemote": {
          "type": "string",
          "description": "it could be one of these;\n- onSite\n- remote\n- hybrid\n\nexample: remote"
        },
        "industryIds": {
          "type": "string",
          "description": "please follow this to find industry id"
        },
        "sort": {
          "type": "string",
          "description": "it could be one of these; mostRelevant, mostRecent"
        },
        "keywords": {
          "type": "string",
          "description": "keywords"
        },
        "jobType": {
          "type": "string",
          "description": "it could be one of these; fullTime, partTime, contract, internship\nExample: contract"
        },
        "start": {
          "type": "string",
          "description": "it could be one of these; 0, 50, 100, 150, 200, etc.\nThe maximum number of start is 975"
        },
        "datePosted": {
          "type": "string",
          "description": "it could be one of these; anyTime, pastMonth, pastWeek, past24Hours"
        }
      },
      "required": [
        "keywords"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Profile_s_Posted_Jobs",
    "description": "Get Profile's Posted Jobs",
    "method": "GET",
    "path": "/profiles/posted-jobs",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "LinkedIn job id"
        }
      },
      "required": [
        "username"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Company_Post_Comments",
    "description": "Get Company Post Comments",
    "method": "GET",
    "path": "/get-company-post-comments",
    "parameters": {
      "type": "object",
      "properties": {
        "sort": {
          "type": "string",
          "description": "sort"
        },
        "page": {
          "type": "string",
          "description": "page"
        },
        "urn": {
          "type": "string",
          "description": "urn"
        }
      },
      "required": [
        "sort",
        "urn"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Company_Employees_Count",
    "description": "Get Company Employees Count",
    "method": "POST",
    "path": "/get-company-employees-count",
    "parameters": {
      "type": "object",
      "properties": {
        "companyId": {
          "type": "string",
          "description": "companyId"
        },
        "locations": {
          "type": "array",
          "description": "locations"
        }
      }
    }
  },
  {
    "name": "agntdata_linkedin_Search_Companies",
    "description": "Search Companies",
    "method": "POST",
    "path": "/companies/search",
    "parameters": {
      "type": "object",
      "properties": {
        "keyword": {
          "type": "string",
          "description": "Search keyword for company name or description"
        },
        "locations": {
          "type": "array",
          "description": "Array of LinkedIn geo IDs to filter by location"
        },
        "companySizes": {
          "type": "array",
          "description": "Company size codes: A (1), B (2-10), C (11-50), D (51-200), E (201-500), F (501-1000), G (1001-5000), H (5001-10000), I (10001+)"
        },
        "hasJobs": {
          "type": "boolean",
          "description": "Filter for companies with active job postings"
        },
        "industries": {
          "type": "array",
          "description": "Array of LinkedIn industry IDs to filter by"
        },
        "page": {
          "type": "integer",
          "description": "Page number for pagination"
        }
      }
    }
  },
  {
    "name": "agntdata_linkedin_Get_Job_Details",
    "description": "Get Job Details",
    "method": "GET",
    "path": "/get-job-details",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "number",
          "description": "id"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Article_Comments",
    "description": "Get Article Comments",
    "method": "GET",
    "path": "/get-article-comments",
    "parameters": {
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "description": "url"
        },
        "page": {
          "type": "string",
          "description": "page"
        },
        "sort": {
          "type": "string",
          "description": "sort"
        }
      },
      "required": [
        "url"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Article_Reactions",
    "description": "Get Article Reactions",
    "method": "GET",
    "path": "/get-article-reactions",
    "parameters": {
      "type": "object",
      "properties": {
        "page": {
          "type": "string",
          "description": "page"
        },
        "url": {
          "type": "string",
          "description": "url"
        }
      },
      "required": [
        "url"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Article",
    "description": "Get Article",
    "method": "GET",
    "path": "/get-article",
    "parameters": {
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "description": "url"
        }
      },
      "required": [
        "url"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_User_Articles",
    "description": "Get User Articles",
    "method": "GET",
    "path": "/get-user-articles",
    "parameters": {
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "description": "url"
        },
        "username": {
          "type": "string",
          "description": "username"
        }
      }
    }
  },
  {
    "name": "agntdata_linkedin_Get_Post_Reposts",
    "description": "Get Post Reposts",
    "method": "POST",
    "path": "/posts/reposts",
    "parameters": {
      "type": "object",
      "properties": {
        "urn": {
          "type": "string",
          "description": "urn"
        },
        "page": {
          "type": "integer",
          "description": "page"
        },
        "paginationToken": {
          "type": "string",
          "description": "paginationToken"
        }
      }
    }
  },
  {
    "name": "agntdata_linkedin_Get_Post",
    "description": "Get Post",
    "method": "GET",
    "path": "/get-post",
    "parameters": {
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "description": "url"
        }
      },
      "required": [
        "url"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Company_Jobs",
    "description": "Get Company Jobs",
    "method": "POST",
    "path": "/company-jobs",
    "parameters": {
      "type": "object",
      "properties": {
        "companyIds": {
          "type": "array",
          "description": "companyIds"
        },
        "page": {
          "type": "integer",
          "description": "page"
        }
      }
    }
  },
  {
    "name": "agntdata_linkedin_Search_Jobs",
    "description": "Search Jobs",
    "method": "GET",
    "path": "/search-jobs",
    "parameters": {
      "type": "object",
      "properties": {
        "sort": {
          "type": "string",
          "description": "it could be one of these; mostRelevant, mostRecent"
        },
        "locationId": {
          "type": "number",
          "description": "please follow this to find location id"
        },
        "titleIds": {
          "type": "string",
          "description": "please follow this to find title id by title"
        },
        "experienceLevel": {
          "type": "string",
          "description": "it could be one of these; internship, associate, director, entryLevel, midSeniorLevel. executive\nexample: executive"
        },
        "functionIds": {
          "type": "string",
          "description": "please follow this to find function id"
        },
        "jobType": {
          "type": "string",
          "description": "it could be one of these; fullTime, partTime, contract, internship\nExample: contract"
        },
        "keywords": {
          "type": "string",
          "description": "keywords"
        },
        "datePosted": {
          "type": "string",
          "description": "it could be one of these; anyTime, pastMonth, pastWeek, past24Hours"
        },
        "salary": {
          "type": "string",
          "description": "it could be one of these; 40k+, 60k+, 80k+, 100k+, 120k+, 140k+, 160k+, 180k+, 200k+\nExample: 80k+"
        },
        "industryIds": {
          "type": "string",
          "description": "please follow this to find industry id"
        },
        "companyIds": {
          "type": "string",
          "description": "please follow this to find company id"
        },
        "onsiteRemote": {
          "type": "string",
          "description": "it could be one of these;\n- onSite\n- remote\n- hybrid\n\nexample: remote"
        },
        "start": {
          "type": "string",
          "description": "it could be one of these; 0, 25, 50, 75, 100, etc.\nThe maximum number of start is 975"
        }
      },
      "required": [
        "keywords"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Health_Check",
    "description": "Health Check",
    "method": "GET",
    "path": "/health",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "agntdata_linkedin_Get_Hiring_Team",
    "description": "Get Hiring Team",
    "method": "GET",
    "path": "/get-hiring-team",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "LinkedIn job id"
        },
        "url": {
          "type": "string",
          "description": "LinkedIn job url"
        }
      }
    }
  },
  {
    "name": "agntdata_linkedin_Search_Locations",
    "description": "Search Locations",
    "method": "GET",
    "path": "/search-locations",
    "parameters": {
      "type": "object",
      "properties": {
        "keyword": {
          "type": "string",
          "description": "keyword"
        }
      },
      "required": [
        "keyword"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Search_Post_by_Hashtag",
    "description": "Search Post by Hashtag",
    "method": "POST",
    "path": "/search-posts-by-hashtag",
    "parameters": {
      "type": "object",
      "properties": {
        "hashtag": {
          "type": "string",
          "description": "hashtag"
        },
        "sortBy": {
          "type": "string",
          "description": "sortBy"
        },
        "start": {
          "type": "string",
          "description": "start"
        },
        "paginationToken": {
          "type": "string",
          "description": "paginationToken"
        }
      }
    }
  },
  {
    "name": "agntdata_linkedin_Get_Company_Jobs_Count",
    "description": "Get Company Jobs Count",
    "method": "GET",
    "path": "/get-company-jobs-count",
    "parameters": {
      "type": "object",
      "properties": {
        "companyId": {
          "type": "string",
          "description": "companyId"
        }
      },
      "required": [
        "companyId"
      ]
    }
  },
  {
    "name": "agntdata_linkedin_Get_Profile_Recent_Activity_Time",
    "description": "Get Profile Recent Activity Time",
    "method": "GET",
    "path": "/get-profile-recent-activity-time",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        }
      },
      "required": [
        "username"
      ]
    }
  }
]
```

## Example

```bash
curl -X GET "https://api.agntdata.dev/v1/data/linkedin/get-company-by-domain?param=value" \
  -H "Authorization: Bearer $AGNTDATA_API_KEY"
```

## Links

- [Documentation](https://agnt.mintlify.app)
- [API Reference](https://agnt.mintlify.app/apis/social/linkedin)
- [Dashboard](https://app.agntdata.dev/dashboard)

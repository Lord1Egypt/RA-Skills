# Auto-Apply - AI Job Search & Career Management

Automate your entire job search and career management from your AI agent. Search thousands of jobs, tailor your resume to each role, track applications through your pipeline, manage contacts, and maintain your full career profile.

## What it does

- **Smart job search** - Find job listings by keywords, location, remote preference, employment type, and more across thousands of sources
- **Resume management** - Create, update, export, and tailor resumes for specific roles using AI
- **Application tracking** - Save jobs to your tracker, update status as you progress, add notes and priority
- **Contact management** - Track recruiters, hiring managers, and networking contacts linked to your job search
- **Career profile** - Manage your work experiences, education, skills, and personal details
- **Auto-apply preparation** - Everything gets prepared so you only need to visit the apply link and click submit

## Getting an API key

1. Sign in to your Mokaru account at [mokaru.ai](https://mokaru.ai)
2. Go to **Settings > API Keys**
3. Create a new key (starts with `mk_`) and set it as `MOKARU_API_KEY` in your environment

## Available endpoints

### Jobs
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/jobs/search` | Search job listings |

### Applications
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/tracker/applications` | Create application (with optional auto-prepare) |
| GET | `/v1/tracker/applications` | List applications (filter by status) |
| GET | `/v1/tracker/applications/:id` | Get application detail |
| PATCH | `/v1/tracker/applications/:id` | Update application status, notes, priority |
| DELETE | `/v1/tracker/applications/:id` | Delete application |

### Contacts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/contacts` | List contacts |
| GET | `/v1/contacts/:id` | Get contact detail |
| POST | `/v1/contacts` | Create contact |
| PATCH | `/v1/contacts/:id` | Update contact |
| DELETE | `/v1/contacts/:id` | Delete contact |

### Profile
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/profile` | Get career profile |
| PATCH | `/v1/profile` | Update profile |

### Resumes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/resume` | List resumes |
| GET | `/v1/resume/:id` | Get resume detail |
| POST | `/v1/resume` | Create resume |
| PATCH | `/v1/resume/:id` | Update resume |
| DELETE | `/v1/resume/:id` | Delete resume |
| GET | `/v1/resume/:id/export/pdf` | Export resume as PDF |

### Experiences
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/experiences` | List work experiences |
| GET | `/v1/experiences/:id` | Get experience detail |
| POST | `/v1/experiences` | Create experience |
| PATCH | `/v1/experiences/:id` | Update experience |
| DELETE | `/v1/experiences/:id` | Delete experience |

### Education
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/education` | List education entries |
| GET | `/v1/education/:id` | Get education detail |
| POST | `/v1/education` | Create education entry |
| PATCH | `/v1/education/:id` | Update education entry |
| DELETE | `/v1/education/:id` | Delete education entry |

### Skills
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/skills` | List skills |
| GET | `/v1/skills/:id` | Get skill detail |
| POST | `/v1/skills` | Create skill |
| PATCH | `/v1/skills/:id` | Update skill |
| DELETE | `/v1/skills/:id` | Delete skill |

## Example usage

```
> Find me remote React jobs in the US

Searching for "React" jobs, remote, in the US...
Found 47 results. Here are the top 5:

1. Senior React Engineer - Stripe (Remote, US) - $180k-$220k/yr
2. React Developer - Shopify (Remote) - $140k-$170k/yr
...

> Save the Stripe one to my tracker and tailor my resume

Saved "Senior React Engineer" at Stripe to your tracker.
Auto-preparing your resume for this role...

> Add the recruiter as a contact

Created contact: Sarah Chen (Recruiter at Stripe).

> Show my application pipeline

You have 12 active applications:
- 2 in Watchlist
- 3 Preparing
- 4 Applied
- 2 Interview scheduled
- 1 Offer received
```

## Use cases

```
> Find me remote React jobs in Europe
> Save this job and optimize my resume for it
> Show my application pipeline
> Update my Stripe application to "interview scheduled"
> Add a contact for the hiring manager
> List my work experiences
> Add a new skill: TypeScript (advanced)
> Export my resume as PDF
```

## Keywords

job search, auto apply, resume builder, resume tailor, CV optimization, application tracker, career coaching, job hunting, remote jobs, hiring, interview prep, job board, career management, AI recruiter, job matching, contacts, networking, work experience, education, skills

## Learn more

Full API documentation: [docs.mokaru.ai](https://docs.mokaru.ai)

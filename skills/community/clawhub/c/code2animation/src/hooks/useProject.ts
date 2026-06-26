import { useState, useEffect } from 'react';

interface ProjectInfo {
  id: string;
  name: string;
  description?: string;
}

export function useProject(initialProject: string) {
  const [projects, setProjects] = useState<any>({});
  const [availableProjects, setAvailableProjects] = useState<ProjectInfo[]>([]);
  const [activeProject, setActiveProject] = useState<string>(initialProject);
  const [isLoadingProject, setIsLoadingProject] = useState(true);

  // Load available projects list on mount
  useEffect(() => {
    const loadAvailableProjects = async () => {
      try {
        const response = await fetch('/api/projects');
        if (response.ok) {
          const data = await response.json();
          setAvailableProjects(data.projects || []);
        } else {
          console.error('Failed to load available projects');
        }
      } catch (error) {
        console.error('Error loading available projects:', error);
      }
    };
    
    loadAvailableProjects();
  }, []);

  // Load project JSON dynamically
  useEffect(() => {
    const loadProject = async () => {
      try {
        setIsLoadingProject(true);
        const response = await fetch(`/projects/${activeProject}.json`);
        if (response.ok) {
          const projectData = await response.json();
          
          // Process background path: convert file to full path
          const processedProject = {
            ...projectData,
            background: projectData.background 
              ? `/projects/${activeProject}/footage/${projectData.background}`
              : projectData.background
          };
          
          setProjects((prev: any) => ({ ...prev, [activeProject]: processedProject }));
        } else {
          console.error(`Failed to load project ${activeProject}`);
        }
      } catch (error) {
        console.error('Error loading project:', error);
      } finally {
        setIsLoadingProject(false);
      }
    };
    
    if (activeProject && !projects[activeProject]) {
      loadProject();
    } else {
      setIsLoadingProject(false);
    }
  }, [activeProject, projects]);

  return {
    projects,
    availableProjects,
    activeProject,
    setActiveProject,
    isLoadingProject,
    currentProject: activeProject ? projects[activeProject] : null
  };
}